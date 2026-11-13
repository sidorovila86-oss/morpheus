param([int]$Port = 8767)
$root = $PSScriptRoot
$types = @{ '.html'='text/html; charset=utf-8'; '.js'='text/javascript'; '.png'='image/png'; '.ogg'='audio/ogg'; '.wav'='audio/wav'; '.ttf'='font/ttf'; '.json'='application/json'; '.css'='text/css'; '.woff2'='font/woff2'; '.gif'='image/gif' }
$l = New-Object System.Net.HttpListener
$l.Prefixes.Add("http://localhost:$Port/"); $l.Start()
Write-Host "serving $root on http://localhost:$Port/"
while ($l.IsListening) {
  $ctx = $l.GetContext()
  $name = [uri]::UnescapeDataString($ctx.Request.Url.AbsolutePath.TrimStart('/')); if (-not $name -or $name.EndsWith("/")) { $name += "index.html" }
  $p = [IO.Path]::GetFullPath((Join-Path $root $name))
  if ($p.StartsWith($root) -and (Test-Path $p -PathType Leaf)) {
    $b = [IO.File]::ReadAllBytes($p); $ext = [IO.Path]::GetExtension($p).ToLower()
    $ctx.Response.ContentType = $(if ($types[$ext]) { $types[$ext] } else { 'application/octet-stream' })
    $ctx.Response.Headers.Add('Cache-Control', 'no-store')
    $ctx.Response.OutputStream.Write($b, 0, $b.Length)
  } else { $ctx.Response.StatusCode = 404 }
  $ctx.Response.Close()
}
