// Pixel-art generator for "Morpheus at the Desk".
// Base resolution 320x180 (shown x4 on a 1280x720 screen). Chunky pixels, one palette, dark night lighting.
// Build: powershell -ExecutionPolicy Bypass -File build.ps1
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

public class Img
{
    public int W, H; public uint[] P;
    public Img(int w, int h) { W = w; H = h; P = new uint[w * h]; }

    static readonly int[,] Bayer = { { 0, 8, 2, 10 }, { 12, 4, 14, 6 }, { 3, 11, 1, 9 }, { 15, 7, 13, 5 } };
    public static float B(int x, int y) { return (Bayer[y & 3, x & 3] + 0.5f) / 16f; }

    public static uint C(string hex) { hex = hex.TrimStart('#'); return Convert.ToUInt32(hex, 16) | 0xFF000000; }
    public static uint CA(string hex, int a) { return (C(hex) & 0x00FFFFFF) | ((uint)a << 24); }

    public bool In(int x, int y) { return x >= 0 && y >= 0 && x < W && y < H; }
    public uint Get(int x, int y) { return In(x, y) ? P[y * W + x] : 0; }

    public void Set(int x, int y, uint c)
    {
        if (!In(x, y)) return;
        uint a = c >> 24;
        if (a == 255) { P[y * W + x] = c; return; }
        if (a == 0) return;
        P[y * W + x] = Mix(P[y * W + x], c, a / 255f);
    }

    static uint Mix(uint d, uint s, float sa)
    {
        float da = (d >> 24) / 255f;
        float oa = sa + da * (1 - sa);
        if (oa <= 0) return 0;
        float r = (((s >> 16) & 255) * sa + ((d >> 16) & 255) * da * (1 - sa)) / oa;
        float g = (((s >> 8) & 255) * sa + ((d >> 8) & 255) * da * (1 - sa)) / oa;
        float b = ((s & 255) * sa + (d & 255) * da * (1 - sa)) / oa;
        return ((uint)(oa * 255 + 0.5f) << 24) | ((uint)(r + 0.5f) << 16) | ((uint)(g + 0.5f) << 8) | (uint)(b + 0.5f);
    }

    public void Tint(int x, int y, uint col, float t)
    {
        if (!In(x, y) || t <= 0) return;
        uint d = P[y * W + x]; if ((d >> 24) == 0) return;
        if (t > 1) t = 1;
        uint m = Mix(d | 0xFF000000, (col & 0x00FFFFFF) | 0xFF000000, t);
        P[y * W + x] = (m & 0x00FFFFFF) | (d & 0xFF000000);
    }

    public void Fill(uint c) { for (int i = 0; i < P.Length; i++) P[i] = c; }
    public void Rect(int x, int y, int w, int h, uint c) { for (int j = y; j < y + h; j++) for (int i = x; i < x + w; i++) Set(i, j, c); }
    public void Clear(int x, int y) { if (In(x, y)) P[y * W + x] = 0; }

    public void Ell(float cx, float cy, float rx, float ry, uint c)
    {
        for (int y = (int)(cy - ry - 1); y <= cy + ry + 1; y++)
            for (int x = (int)(cx - rx - 1); x <= cx + rx + 1; x++)
            {
                float dx = (x + 0.5f - cx) / rx, dy = (y + 0.5f - cy) / ry;
                if (dx * dx + dy * dy <= 1) Set(x, y, c);
            }
    }
    public void Ring(float cx, float cy, float ro, float ri, uint c)
    {
        for (int y = (int)(cy - ro - 1); y <= cy + ro + 1; y++)
            for (int x = (int)(cx - ro - 1); x <= cx + ro + 1; x++)
            {
                float d = (float)Math.Sqrt((x + 0.5f - cx) * (x + 0.5f - cx) + (y + 0.5f - cy) * (y + 0.5f - cy));
                if (d <= ro && d > ri) Set(x, y, c);
            }
    }
    public void Line(float x0, float y0, float x1, float y1, uint c, int th)
    {
        float dx = x1 - x0, dy = y1 - y0; int n = (int)Math.Max(Math.Abs(dx), Math.Abs(dy)); if (n == 0) n = 1;
        for (int i = 0; i <= n; i++)
        {
            int x = (int)Math.Round(x0 + dx * i / n), y = (int)Math.Round(y0 + dy * i / n);
            Rect(x - th / 2, y - th / 2, th, th, c);
        }
    }

    public void Outline(uint c)
    {
        bool[] m = new bool[P.Length];
        for (int i = 0; i < P.Length; i++) m[i] = (P[i] >> 24) > 0;
        for (int y = 0; y < H; y++) for (int x = 0; x < W; x++)
            {
                if (m[y * W + x]) continue;
                bool n = (x > 0 && m[y * W + x - 1]) || (x < W - 1 && m[y * W + x + 1]) || (y > 0 && m[(y - 1) * W + x]) || (y < H - 1 && m[(y + 1) * W + x]);
                if (n) P[y * W + x] = c;
            }
    }
    public void InnerOutline(uint c)
    {
        bool[] m = new bool[P.Length];
        for (int i = 0; i < P.Length; i++) m[i] = (P[i] >> 24) > 0;
        for (int y = 0; y < H; y++) for (int x = 0; x < W; x++)
            {
                if (!m[y * W + x]) continue;
                bool edge = x == 0 || y == 0 || x == W - 1 || y == H - 1 || !m[y * W + x - 1] || !m[y * W + x + 1] || !m[(y - 1) * W + x] || !m[(y + 1) * W + x];
                if (edge) P[y * W + x] = c;
            }
    }

    public void Blit(Img s, int ox, int oy) { for (int y = 0; y < s.H; y++) for (int x = 0; x < s.W; x++) Set(ox + x, oy + y, s.P[y * s.W + x]); }

    public void VGrad(int x0, int y0, int w, int h, uint[] cols)
    {
        for (int y = y0; y < y0 + h; y++)
        {
            float f = (float)(y - y0) / Math.Max(1, h - 1) * (cols.Length - 1);
            int i = (int)Math.Floor(f); if (i >= cols.Length - 1) i = cols.Length - 2; float fr = f - i;
            for (int x = x0; x < x0 + w; x++) Set(x, y, fr > B(x, y) ? cols[i + 1] : cols[i]);
        }
    }

    public Img Scale(int n)
    {
        Img o = new Img(W * n, H * n);
        for (int y = 0; y < o.H; y++) for (int x = 0; x < o.W; x++) o.P[y * o.W + x] = P[(y / n) * W + x / n];
        return o;
    }

    public void Save(string path)
    {
        using (Bitmap bmp = new Bitmap(W, H, PixelFormat.Format32bppArgb))
        {
            BitmapData bd = bmp.LockBits(new Rectangle(0, 0, W, H), ImageLockMode.WriteOnly, PixelFormat.Format32bppArgb);
            int[] buf = new int[P.Length]; Buffer.BlockCopy(P, 0, buf, 0, P.Length * 4);
            for (int y = 0; y < H; y++) Marshal.Copy(buf, y * W, bd.Scan0 + y * bd.Stride, W);
            bmp.UnlockBits(bd);
            bmp.Save(path, ImageFormat.Png);
        }
    }
}

public static class Pal
{
    static uint X(string h) { return Img.C(h); }
    public static readonly uint Void = X("0b0a10"), Night = X("12101a"), Night2 = X("1a1826"), Wall = X("221f30"), Wall2 = X("272437"),
        Office = X("262636"), Hall = X("34354a"), Hall2 = X("2c2d40"), Hall3 = X("232333"), UI = X("3f3b55"), Frame = X("110f17"), Frame2 = X("221f2e"),
        Plum = X("4e4068"), Plum2 = X("332c4c"), Plate = X("231f35"),
        Wood0 = X("1e1712"), Wood1 = X("3a2d23"), Wood2 = X("4a3a2c"), Wood3 = X("5c4a38"), Wood4 = X("6b5843"), Wood5 = X("7a6650"), Wood6 = X("8a755c"), Wood7 = X("9c876b"),
        Paper = X("e6dcc4"), Paper2 = X("cbbf9f"), Paper3 = X("a8997a"), Paper4 = X("d9cdb0"), PaperW = X("f2ecdc"), Ink = X("221e2b"),
        Fluoro = X("d4e2c2"), Fluoro2 = X("8fa88b"),
        Blue0 = X("1a2238"), Blue1 = X("2d3f61"), Blue2 = X("4f679a"), Blue3 = X("8ea3cc"), Blue4 = X("bccbe6"), Blue5 = X("dde6f5"),
        G0 = X("24543a"), G1 = X("3f8259"), G2 = X("6cb07e"), R0 = X("651f1d"), R1 = X("ad3832"), R2 = X("d9645a"),
        Sticky = X("e8c94e"), Sticky2 = X("d4b23e"), Sticky3 = X("a8892c"),
        D1 = X("2b2154"), D2 = X("45327a"), D3 = X("6a4a9c"), D4 = X("945fb6"), D5 = X("c07ec0"), D6 = X("eaa0c2"), Pink = X("f0aec2"), Cloud = X("fbdbe9"),
        Lav = X("ab95dc"), Lav2 = X("e4d6ff"), Lav3 = X("a893e0"), Cyan = X("8ccbdc"), Star = X("f6e7a1"), Gold = X("e0ad42"), Gold2 = X("b36f18"),
        Robe = X("222a54"), Robe2 = X("161c3c"), Robe3 = X("303b72"), Mug = X("e2dac6"), Mug2 = X("bdb39b"), Coffee = X("4e3220"), Coffee2 = X("34210f"),
        Skin = X("e0b99c"), Skin2 = X("bc927a"), Steel = X("8e8a96"), Steel2 = X("c4c3ce"), Dark = X("332e3d"), Handle = X("241b22"),
        Cork = X("7e5d3b"), Cork2 = X("5f442a"), Terra = X("9a4d33"), Terra2 = X("b55e40"), Terra3 = X("6d3523"),
        Leaf0 = X("17392a"), Leaf1 = X("265a3c"), Leaf2 = X("3f855b"), Leaf3 = X("68b07e"), White = X("ffffff"),
        Slip = X("eeeadf"), Slip2 = X("e0dacb"), Slip3 = X("8d86a0"), Sil = X("16151f"), Sil2 = X("252436");
}

public static class Art
{
    static Random R = new Random(7);
    static float B(int x, int y) { return Img.B(x, y); }

    // Light sources in base (320x180) coordinates: x, y, radius, intensity, r, g, b
    public static readonly float[,] Lights = {
        { 150, 148, 128, 0.95f, 1.00f, 0.78f, 0.50f },   // desk lamp, warm, centre of the desk
        { 268,  59,  90, 0.95f, 0.85f, 0.55f, 0.95f },   // dream door
        { 272, 124,  76, 0.55f, 0.90f, 0.52f, 0.85f },   // door spill on the desk
        { 125,  28,  86, 0.55f, 0.65f, 0.85f, 0.78f },   // last working hallway lamp
    };
    public static readonly float[] Ambient = { 0.17f, 0.16f, 0.28f };

    public static void Light(Img g, int y0, int y1, Func<int, int, bool> skip)
    {
        for (int y = y0; y < y1; y++) for (int x = 0; x < g.W; x++)
            {
                if (skip != null && skip(x, y)) continue;
                uint c = g.P[y * g.W + x]; if ((c >> 24) == 0) continue;
                float lr = Ambient[0], lg = Ambient[1], lb = Ambient[2];
                for (int i = 0; i < Lights.GetLength(0); i++)
                {
                    float dx = x - Lights[i, 0], dy = y - Lights[i, 1]; float d = (float)Math.Sqrt(dx * dx + dy * dy);
                    if (d >= Lights[i, 2]) continue;
                    float f = 1 - d / Lights[i, 2]; f = f * f * Lights[i, 3];
                    lr += f * Lights[i, 4]; lg += f * Lights[i, 5]; lb += f * Lights[i, 6];
                }
                float b = B(x, y);
                lr = (float)Math.Floor(Math.Min(1.1f, lr) * 6 + b) / 6f; lg = (float)Math.Floor(Math.Min(1.1f, lg) * 6 + b) / 6f; lb = (float)Math.Floor(Math.Min(1.1f, lb) * 6 + b) / 6f;
                int r = (int)Math.Min(255, ((c >> 16) & 255) * lr), gg = (int)Math.Min(255, ((c >> 8) & 255) * lg), bb = (int)Math.Min(255, (c & 255) * lb);
                g.P[y * g.W + x] = (c & 0xFF000000) | ((uint)r << 16) | ((uint)gg << 8) | (uint)bb;
            }
    }
    static bool DreamHole(int x, int y) { return x >= 251 && x < 286 && y >= 24 && y < 94; }

    // ------------------------------------------------------------------ ROOM
    public static Img Room()
    {
        Img g = new Img(320, 180); g.Fill(Pal.Night2);

        g.Rect(0, 13, 320, 87, Pal.Wall);
        for (int x = 0; x < 320; x += 24) g.Rect(x, 13, 1, 87, Pal.Wall2);

        // hallway
        int hx0 = 8, hy0 = 16, hx1 = 232, hy1 = 100;
        g.VGrad(hx0, hy0, hx1 - hx0, 66, new uint[] { Pal.Hall2, Pal.Hall });
        g.Rect(hx0, 82, hx1 - hx0, 1, Pal.Hall3);
        g.Rect(hx0, 83, hx1 - hx0, hy1 - 83, Pal.Office);
        for (int y = 86; y < hy1; y += 4) g.Rect(hx0, y, hx1 - hx0, 1, Pal.Hall3);
        for (int vx = -200; vx <= 450; vx += 30)
            for (int y = 83; y < hy1; y++) { float t = (y - 60f) / (hy1 - 60f); int x = (int)(120 + (vx - 120) * t); if (x >= hx0 && x < hx1) g.Set(x, y, Pal.Hall3); }

        // far door, notice board, clock
        g.Rect(191, 49, 23, 34, Pal.Frame2); g.Rect(193, 51, 19, 32, Pal.Office); g.Rect(199, 54, 7, 5, Pal.Hall2); g.Set(209, 66, Pal.Steel);
        g.Rect(54, 38, 29, 21, Pal.Cork2); g.Rect(55, 39, 27, 19, Pal.Cork);
        int[,] nt = { { 57, 41, 7, 6 }, { 66, 40, 6, 8 }, { 74, 42, 6, 5 }, { 59, 49, 8, 6 }, { 70, 50, 9, 6 } };
        for (int i = 0; i < 5; i++) { g.Rect(nt[i, 0], nt[i, 1], nt[i, 2], nt[i, 3], i % 2 == 0 ? Pal.Paper : Pal.Fluoro2); g.Set(nt[i, 0] + nt[i, 2] / 2, nt[i, 1], Pal.R1); }
        g.Ell(160, 33, 5, 5, Pal.Frame2); g.Ell(160, 33, 4, 4, Pal.Paper2); g.Set(160, 31, Pal.Ink); g.Set(160, 32, Pal.Ink); g.Set(161, 33, Pal.Ink);

        // lamps: only the middle one works
        g.Rect(15, 17, 37, 2, Pal.UI); g.Rect(170, 17, 32, 2, Pal.UI);
        g.Rect(102, 17, 45, 2, Pal.Fluoro); g.Rect(102, 19, 45, 1, Pal.Fluoro2);

        // glass sheen on the middle pane
        for (int y = hy0; y < hy1; y++) for (int x = 94; x < 227; x++)
            {
                int k = ((x - (int)(y * 0.9f)) % 70 + 70) % 70;
                if (k < 6) g.Tint(x, y, Pal.White, 0.08f); else if (k == 8) g.Tint(x, y, Pal.White, 0.06f);
            }

        // frame + mullions
        g.Rect(hx0 - 3, hy0 - 3, hx1 - hx0 + 6, 3, Pal.Frame);
        g.Rect(hx0 - 3, hy0, 3, hy1 - hy0, Pal.Frame); g.Rect(hx1, hy0, 3, hy1 - hy0, Pal.Frame);
        g.Rect(90, hy0, 4, hy1 - hy0, Pal.Frame); g.Rect(227, hy0, 4, hy1 - hy0, Pal.Frame);

        // dream door
        g.Rect(247, 20, 43, 78, Pal.Plum2); g.Rect(248, 21, 41, 76, Pal.Frame); g.Rect(251, 24, 35, 70, Img.C("100d1a"));
        g.Rect(248, 21, 41, 1, Pal.Plum);

        // sign plate
        g.Rect(293, 35, 23, 26, Pal.UI); g.Rect(294, 36, 21, 24, Pal.Plate);
        g.Set(304, 56, Pal.Lav); g.Set(304, 55, Pal.Star);

        // counter + slot
        g.Rect(0, 100, 320, 7, Pal.Wood1); g.Rect(0, 100, 320, 1, Pal.Wood3);
        for (int x = 0; x < 320; x += 2) if (R.Next(4) == 0) g.Rect(x, 102 + R.Next(4), R.Next(4) + 1, 1, Pal.Wood2);
        g.Rect(125, 102, 36, 1, Pal.Wood3); g.Rect(125, 103, 36, 2, Pal.Void);
        g.Rect(0, 106, 320, 1, Pal.Wood0);

        // desk
        g.Rect(0, 107, 320, 59, Pal.Wood5);
        for (int y = 107; y < 163; y += 14) { g.Rect(0, y + 13, 320, 1, Pal.Wood3); }
        for (int i = 0; i < 110; i++) { int y = 108 + R.Next(55); int x = R.Next(320); g.Rect(x, y, 3 + R.Next(14), 1, R.Next(3) == 0 ? Pal.Wood6 : Pal.Wood4); }
        for (int i = 0; i < 4; i++) { int kx = 20 + R.Next(280), ky = 112 + R.Next(48); g.Ring(kx, ky, 2.5f, 1.4f, Pal.Wood4); g.Set(kx, ky, Pal.Wood3); }
        g.Rect(0, 163, 320, 1, Pal.Wood6); g.Rect(0, 164, 320, 2, Pal.Wood2);
        for (int y = 107; y < 113; y++) for (int x = 0; x < 320; x++) if ((y - 107) / 6f < B(x, y)) g.Tint(x, y, Pal.Void, 0.5f);

        // plant
        g.Blit(Plant(), 1, 59);

        // lighting
        Light(g, 13, 166, DreamHole);
        // door glow on the wall (after lighting so it reads as emitted light)
        for (int y = 13; y < 100; y++) for (int x = 232; x < 320; x++)
            {
                if (DreamHole(x, y)) continue;
                float dx = x - 268.5f, dy = (y - 59) * 0.7f; float d = (float)Math.Sqrt(dx * dx + dy * dy);
                float t = Math.Max(0, 1 - d / 46f); t = (float)Math.Floor(t * t * 4 + B(x, y)) / 4f;
                if (t > 0) g.Tint(x, y, Pal.D5, t * 0.45f);
            }

        // bars
        g.Rect(0, 0, 320, 12, Pal.Void); g.Rect(0, 12, 320, 1, Img.C("06050a"));
        g.Rect(0, 166, 320, 14, Pal.Void); g.Rect(3, 167, 314, 12, Img.C("1f1b2e")); g.Rect(4, 168, 312, 10, Img.C("0a0910"));

        // vignette
        for (int y = 13; y < 166; y++) for (int x = 0; x < 320; x++)
            {
                float dx = (x - 160) / 160f, dy = (y - 100) / 90f; float d = (float)Math.Sqrt(dx * dx + dy * dy) - 0.62f;
                if (d > 0) { float t = (float)Math.Floor(d * 1.5f * 4 + B(x, y)) / 4f; g.Tint(x, y, Img.C("050408"), Math.Min(0.75f, t)); }
            }
        return g;
    }

    static Img Plant()
    {
        Img p = new Img(32, 45);
        float[,] lv = { { 16, 11, 3, 9, -0.2f }, { 9, 15, 3, 8, -0.9f }, { 23, 15, 3, 8, 0.9f }, { 5, 23, 2.5f, 6.5f, -1.3f }, { 27, 23, 2.5f, 6.5f, 1.3f }, { 12, 20, 3, 8, -0.5f }, { 20, 20, 3, 8, 0.5f } };
        for (int i = 0; i < lv.GetLength(0); i++)
        {
            float cx = lv[i, 0], cy = lv[i, 1], rx = lv[i, 2], ry = lv[i, 3], a = lv[i, 4];
            float ca = (float)Math.Cos(a), sa = (float)Math.Sin(a);
            for (int y = 0; y < 32; y++) for (int x = 0; x < 32; x++)
                {
                    float dx = x + 0.5f - cx, dy = y + 0.5f - cy; float u = dx * ca + dy * sa, v = -dx * sa + dy * ca;
                    float q = (u * u) / (rx * rx) + (v * v) / (ry * ry);
                    if (q <= 1) p.Set(x, y, u < 0 ? Pal.Leaf1 : (q < 0.4f && v < 0 ? Pal.Leaf3 : Pal.Leaf2));
                }
        }
        for (int y = 29; y < 44; y++) { int ins = (y - 29) / 4; p.Rect(7 + ins, y, 18 - ins * 2, 1, Pal.Terra); p.Set(7 + ins, y, Pal.Terra2); p.Rect(22 - ins, y, 3, 1, Pal.Terra3); }
        p.Rect(5, 28, 22, 3, Pal.Terra2); p.Rect(5, 30, 22, 1, Pal.Terra3);
        p.Outline(Pal.Leaf0);
        return p;
    }

    // ------------------------------------------------------------- DESK ITEMS
    public static Img Folder()
    {
        Img f = new Img(84, 59);
        uint T = Img.C("b48c52"), T2 = Img.C("8f6a38"), TO = Img.C("4f3418");
        f.Rect(4, 0, 27, 5, T);
        f.Rect(0, 3, 84, 56, T); f.Rect(0, 56, 84, 3, T2); f.Rect(82, 3, 2, 56, T2);
        f.Rect(4, 2, 75, 3, Pal.Paper4);
        f.Rect(2, 5, 79, 51, Pal.Paper); f.Rect(80, 5, 1, 51, Pal.Paper2); f.Rect(2, 55, 79, 1, Pal.Paper2);
        for (int i = 0; i < 30; i++) f.Set(3 + R.Next(76), 6 + R.Next(48), Pal.Paper4);
        f.Rect(5, 12, 73, 1, Pal.Paper3);
        f.Ring(70, 47, 5, 3.6f, Img.C("c4a57c")); f.Rect(64, 44, 3, 3, Pal.Paper);
        f.Rect(63, 1, 1, 8, Pal.Steel); f.Rect(66, 1, 1, 10, Pal.Steel); f.Rect(64, 0, 2, 1, Pal.Steel); f.Rect(64, 10, 2, 1, Pal.Steel);
        f.Outline(TO);
        return f;
    }

    public static Img StickyNote()
    {
        Img s = new Img(39, 20);
        s.Rect(0, 2, 39, 18, Pal.Sticky); s.Rect(0, 17, 39, 3, Pal.Sticky2);
        for (int i = 0; i < 4; i++) s.Rect(35 + i, 16 + i, 4 - i, 1, 0);
        s.Rect(14, 0, 10, 4, Img.CA("ffffff", 140));
        s.Outline(Pal.Sticky3);
        return s;
    }

    public static Img IdCard(bool crooked)
    {
        Img c = new Img(57, 37);
        uint h = crooked ? Pal.Plum : Pal.Blue1, h2 = crooked ? Img.C("6c5b8c") : Pal.Blue2;
        uint top = crooked ? Img.C("e6ddf0") : Pal.Blue5, bot = crooked ? Img.C("cbbfdc") : Pal.Blue4, line = crooked ? Img.C("3d3155") : Pal.Blue0;
        c.VGrad(0, 0, 57, 37, new uint[] { top, bot });
        c.Rect(0, 0, 57, 6, h); c.Rect(0, 1, 57, 1, h2);
        c.Clear(0, 0); c.Clear(56, 0); c.Clear(0, 36); c.Clear(56, 36);
        int px = crooked ? 4 : 3, py = crooked ? 9 : 8;
        c.Rect(px, py, 26, 26, h); c.Rect(px + 1, py + 1, 24, 24, crooked ? Img.C("b8a8d4") : Pal.Blue3);
        if (crooked) { c.Line(2, 8, 6, 10, Img.CA("efe6c6", 220), 2); c.Line(24, 34, 28, 31, Img.CA("efe6c6", 220), 2); for (int i = 0; i < 6; i++) c.Set(33 + R.Next(18), 24 + R.Next(6), Img.CA("7a6a98", 140)); }
        for (int i = 0; i < 16; i++) if ((i * 7 + i / 3) % 5 < 3) c.Rect(31 + i, 31, 1, 3, h);
        c.Ell(52, 32, 2.6f, 2.6f, crooked ? Img.C("c4a2e4") : Pal.Cyan); c.Set(52, 32, Pal.White);
        c.InnerOutline(line);
        return c;
    }

    public static Img Notebook()
    {
        Img n = new Img(68, 55);
        n.Rect(0, 0, 68, 55, Pal.UI); n.Rect(0, 53, 68, 2, Pal.Plum2);
        n.Rect(4, 1, 63, 52, Pal.PaperW);
        for (int y = 10; y < 52; y += 5) n.Rect(5, y, 61, 1, Pal.Blue4);
        n.Rect(11, 2, 1, 50, Img.C("d9958c"));
        n.Rect(5, 8, 61, 1, Pal.Paper3);
        for (int i = 0; i < 5; i++) n.Rect(66 - i, 48 + i, i + 1, 1, Pal.Paper2);
        for (int y = 3; y < 52; y += 6) { n.Rect(1, y, 5, 1, Pal.Steel2); n.Rect(1, y + 1, 5, 1, Pal.Steel); n.Set(6, y, Pal.UI); }
        n.InnerOutline(Pal.Ink);
        return n;
    }

    public static Img Stamp(bool admit)
    {
        Img s = new Img(38, 22);
        uint c0 = admit ? Pal.G0 : Pal.R0, c1 = admit ? Pal.G1 : Pal.R1, c2 = admit ? Pal.G2 : Pal.R2;
        s.Ell(19, 4, 6.5f, 4.2f, Pal.Wood2); s.Ell(17, 3, 2.5f, 1.5f, Pal.Wood4);
        s.Rect(16, 6, 6, 4, Pal.Wood1);
        s.Rect(9, 9, 20, 2, Pal.Ink);
        s.Rect(1, 11, 36, 8, c1); s.Rect(1, 11, 36, 1, c2); s.Rect(1, 11, 1, 8, c2); s.Rect(1, 17, 36, 2, c0); s.Rect(36, 11, 1, 8, c0);
        s.Rect(10, 13, 18, 4, c0);
        s.Rect(2, 19, 34, 2, Pal.Ink);
        s.Outline(Pal.Void);
        return s;
    }

    public static Img Lens()
    {
        Img l = new Img(31, 31);
        l.Line(19, 19, 28, 28, Pal.Handle, 3); l.Line(18, 18, 20, 20, Pal.Paper3, 3);
        for (int y = 0; y < 31; y++) for (int x = 0; x < 31; x++)
            {
                float d = (float)Math.Sqrt((x + 0.5f - 12) * (x + 0.5f - 12) + (y + 0.5f - 12) * (y + 0.5f - 12));
                if (d <= 8) { float t = (x + y) / 24f; l.Set(x, y, t > 0.6f + B(x, y) * 0.3f ? Pal.Blue2 : (t > 0.35f + B(x, y) * 0.3f ? Pal.Blue3 : Pal.Cyan)); }
            }
        l.Ring(12, 12, 10.5f, 8, Pal.Dark);
        l.Set(8, 7, Pal.White); l.Set(7, 8, Pal.White); l.Set(9, 6, Pal.White);
        l.Outline(Pal.Void);
        return l;
    }

    public static Img MugImg(bool full)
    {
        Img m = new Img(25, 27);
        m.Ring(20, 15, 4.6f, 2.4f, Pal.Mug);
        for (int y = 6; y < 25; y++) { int ins = y > 23 ? 1 : 0; m.Rect(2 + ins, y, 17 - ins * 2, 1, Pal.Mug); m.Rect(15, y, 4 - ins, 1, Pal.Mug2); }
        m.Ell(10.5f, 6, 8.5f, 2.3f, Pal.PaperW); m.Ell(10.5f, 6.3f, 7, 1.6f, full ? Pal.Coffee : Pal.Mug2);
        int sx = 9, sy = 14;
        m.Rect(sx, sy - 2, 1, 5, Pal.Gold); m.Rect(sx - 2, sy, 5, 1, Pal.Gold); m.Set(sx + 1, sy + 1, Pal.Gold2);
        m.Outline(Pal.Ink);
        return m;
    }

    public static Img SlipImg()
    {
        Img s = new Img(46, 32);
        s.Rect(0, 0, 46, 32, Pal.Slip); s.Rect(0, 0, 4, 32, Pal.Slip2); s.Rect(42, 0, 4, 32, Pal.Slip2);
        for (int y = 2; y < 32; y += 4) { s.Set(2, y, Pal.Slip3); s.Set(43, y, Pal.Slip3); }
        for (int x = 0; x < 46; x += 2) { s.Clear(x, 0); s.Clear(x + 1, 31); }
        s.Rect(6, 8, 34, 1, Pal.Paper3);
        s.Outline(Pal.Slip3);
        return s;
    }

    public static Img SleeveImg()
    {
        Img s = new Img(52, 26);
        for (int i = 0; i <= 40; i++)
        {
            float x = i, y = 26 - i * 0.42f;
            for (int k = -7; k <= 7; k++) s.Set((int)(x + k * 0.38f), (int)(y + k), k > 3 ? Pal.Robe2 : (k < -5 ? Pal.Robe3 : Pal.Robe));
        }
        Random r2 = new Random(3);
        for (int i = 0; i < 10; i++) { int x = r2.Next(40), y = r2.Next(26); if ((s.Get(x, y) >> 24) > 0) s.Set(x, y, Pal.Star); }
        for (int k = -7; k <= 7; k++) { s.Set((int)(39 + k * 0.38f), (int)(9 + k), Pal.Gold); s.Set((int)(40 + k * 0.38f), (int)(9 + k), Pal.Gold2); }
        s.Ell(45, 8, 4.5f, 4, Pal.Skin); s.Rect(46, 10, 3, 2, Pal.Skin2); s.Rect(47, 4, 3, 1, Pal.Skin);
        s.Outline(Pal.Void);
        return s;
    }

    public static Img Silhouette()
    {
        Img s = new Img(19, 40);
        s.Ell(9.5f, 6, 5, 5.8f, Pal.Sil);
        s.Ell(9.5f, 41, 9.5f, 28, Pal.Sil);
        for (int y = 0; y < 40; y++) for (int x = 18; x > 0; x--) if ((s.Get(x, y) >> 24) > 0) { s.Set(x, y, Pal.Sil2); break; }
        return s;
    }

    // ----------------------------------------------------------------- DREAMS
    public static Img DreamStairs()
    {
        Img d = new Img(35, 70);
        d.VGrad(0, 0, 35, 70, new uint[] { Pal.D1, Pal.D2, Pal.D3, Pal.D4, Pal.D5, Pal.D6 });
        Random r = new Random(11);
        for (int i = 0; i < 14; i++) d.Set(r.Next(35), r.Next(40), i % 4 == 0 ? Pal.Star : Pal.Cloud);
        float[,] cl = { { 5, 64, 8, 3.5f }, { 21, 67, 11, 4 }, { 33, 62, 7, 3 }, { 3, 45, 5, 2 } };
        for (int i = 0; i < 4; i++) { d.Ell(cl[i, 0], cl[i, 1], cl[i, 2], cl[i, 3], Pal.Pink); d.Ell(cl[i, 0] - 1, cl[i, 1] - 1, cl[i, 2] - 2, cl[i, 3] - 1, Pal.Cloud); }
        for (int i = 0; i < 9; i++) { int x = 3 + i * 3, y = 60 - i * 3; d.Rect(x, y, 4, 1, Pal.Lav2); d.Rect(x, y + 1, 4, 1, Pal.Lav3); }
        for (int i = 0; i < 6; i++) { int x = 26 - i * 3, y = 32 - i * 3; d.Rect(x, y, 4, 1, Pal.Lav2); d.Rect(x, y + 1, 4, 1, Pal.Lav3); }
        for (int i = 0; i < 4; i++) { int x = 16 + i * 3, y = 3 + i * 3; d.Rect(x, y + 1, 4, 1, Pal.Lav2); d.Rect(x, y, 4, 1, Pal.Lav3); }
        d.Rect(6, 9, 4, 6, Pal.Plum); d.Rect(7, 10, 2, 5, Pal.Star);
        return d;
    }

    // ----------------------------------------------------------------- BUILD
    public static void Build(string outDir)
    {
        System.IO.Directory.CreateDirectory(outDir);
        foreach (string f in System.IO.Directory.GetFiles(outDir, "*.png")) System.IO.File.Delete(f);
        Img room = Room(); room.Save(outDir + "/room.png");
        Img dream = DreamStairs(); dream.Save(outDir + "/dream_day3.png");
        Img folder = Folder(); folder.Save(outDir + "/file.png");
        Img sticky = StickyNote(); sticky.Save(outDir + "/sticky.png");
        Img id = IdCard(false); id.Save(outDir + "/idcard.png");
        IdCard(true).Save(outDir + "/idcard_crooked.png");
        Img nb = Notebook(); nb.Save(outDir + "/notebook.png");
        Img sa = Stamp(true); sa.Save(outDir + "/stamp_admit.png");
        Img sd = Stamp(false); sd.Save(outDir + "/stamp_deny.png");
        Img lens = Lens(); lens.Save(outDir + "/lens.png");
        Img mug = MugImg(true); mug.Save(outDir + "/mug.png");
        MugImg(false).Save(outDir + "/mug_empty.png");
        SlipImg().Save(outDir + "/slip.png");
        Img sleeve = SleeveImg(); sleeve.Save(outDir + "/sleeve.png");
        Img sil = Silhouette(); sil.Save(outDir + "/silhouette.png");

        // preview: items get the same lighting as the room
        Img items = new Img(320, 180);
        items.Blit(sil, 60, 60); items.Blit(sil, 46, 62); items.Blit(sil, 32, 60);
        items.Blit(folder, 5, 108); items.Blit(sticky, 46, 146);
        items.Blit(id, 94, 119); items.Blit(nb, 154, 110); items.Blit(sa, 224, 113); items.Blit(sd, 226, 140);
        items.Blit(lens, 270, 136); items.Blit(mug, 292, 106); items.Blit(sleeve, -6, 150);
        Light(items, 0, 180, null);
        Img pv = new Img(320, 180); pv.Blit(room, 0, 0); pv.Blit(dream, 251, 24); pv.Blit(items, 0, 0);
        pv.Save(outDir + "/preview.png"); pv.Scale(4).Save(outDir + "/preview_x4.png");
    }
}
