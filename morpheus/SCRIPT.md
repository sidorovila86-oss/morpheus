# MORPHEUS AT THE DESK — сюжет и диалоги

> Рабочее название. Варианты: *Dream Access Desk*, *Window 3*, *Sweet Dreams, Please*.
>
> Пояснения для разработки — на русском. **Весь игровой текст — на английском** (основной язык).
> Перевод на японский и русский делаем отдельной таблицей локализации, когда текст утвердим.
>
> Год в игре: **2026**. Все места — реальные города мира, но школы, кафе и т.п. выдуманы.

---

## 0. Сеттинг в двух словах

Морфей, бог сновидений, пережил «реструктуризацию». Сны теперь — регулируемая сфера, и Морфея посадили
младшим клерком в **Department of Dream Access**, окошко №3.

Каждую ночь у него **один клиент (Dreamer)** — человек, который спит. На столе досье: короткая биография клиента.
К окошку подходят люди, которые хотят попасть в его сон, и рассказывают, **где и когда познакомились** с клиентом.
Морфей сверяет рассказ с досье, ставит штамп **ADMIT** или **DENY**.

Тон — офисная комедия. Морфей древний, драматичный, уставший и саркастичный, но в глубине души
добрый. Люди у окошка — то смешные, то трогательные.

### Сквозные персонажи

- **Morpheus** — герой, голос в мыслях (реплики курсивом / облачка над столом).
- **Management** — начальство, пишет служебные записки (MEMO). Никогда не появляется лично. Сухой корпоративный стиль.
- **Kevin** — приходит **каждый день** к любому клиенту, каждый раз с поддельным удостоверением
  (разная фамилия, разный год рождения) и неправдоподобной историей. Игрок учится его отшивать.
  **В день 5 Kevin говорит правду**, и это главный поворот игры.

### Деньги

- +5 монет за правильное решение, −5 за ошибку.
- В конце дня: кофе (3 монеты). Если не купил, следующий день идёт без кофе
  (опционально: досье слегка размыто / Морфей зевает в репликах). Чисто для вкуса, можно вырезать.

### Как работает проверка (общий формат посетителя)

У каждого посетителя:
- **ID** — имя, год рождения, откуда.
- **Claim** — первая фраза: как познакомились.
- **3 вопроса**, которые игрок может задать кнопками: **When? / Where exactly? / Who else was there?**
- **Verdict** — правильный ответ.
- **Contradiction** — какие строки досье/ID противоречат (для механики «указать противоречие»).
- **Admit / Deny** — реплика посетителя на решение.
- **Caught** — реплика, если игрок указал противоречие (только у лжецов).
- **If wrong** — строка в утреннем отчёте, если игрок ошибся.

**Железное правило дизайна:** честные посетители никогда не противоречат досье (кроме допуска из правил дня 4).
Лжец всегда противоречит хотя бы одной строке — или его встречи просто нет в досье.

---

## 1. Пролог

**MEMO**
> **DEPARTMENT OF DREAM ACCESS**
> To: Morpheus, God of Dreams *(Junior Access Clerk, Window 3)*
>
> Following the recent restructuring, unsupervised dream visits are no longer permitted.
>
> Each night you will be assigned ONE Dreamer. Visitors will state how they know the Dreamer.
> If their story matches the Dreamer's file — **ADMIT**.
> If it does not, or cannot be confirmed — **DENY**.
>
> Correct decision: +5 coins. Incorrect decision: −5 coins.
> The coffee machine accepts coins.
>
> Welcome aboard.
> — Management

**MORPHEUS**
> *Three thousand years of shaping the dreams of mortals.*
> *Kings wept at my visions. Prophets built temples to my name.*
> *...And now I have a stapler.*
> *Fine. Let's see who's sleeping tonight.*

---

## 2. ДЕНЬ 1 — Emma

**Новое правило:** встреча должна совпадать с досье по месту и времени. Если встречи нет в досье — DENY.

**MEMO**
> Rule #1: The visitor's story must match the Dreamer's file (place AND time).
> If the meeting is not in the file, it did not happen.
> — Management

**MORPHEUS (утро)**
> *Emma Walsh. Thirty-four. Dreams tonight about... a bakery that is also a library. Respectable.*

### Досье

> **DREAMER: Emma Walsh** — born 1992
> - 1992 — Born in Bristol, UK
> - 1998–2010 — St. Anne's School, Bristol
> - 2010–2014 — University of Edinburgh, Journalism
> - 2014–2016 — Barista at Moonbean Café, Edinburgh
> - 2016 — Moved to Dublin. Editor at Greenleaf Books
> - 2019 — Married Tom Walsh
> - 2020– — Climbing gym "The Wall", Dublin

### 1.1 Sam Porter — ✅ ADMIT
**ID:** Sam Porter, born 1992, Bristol
- **Claim:** "Hi! Emma and I were in the same class at St. Anne's. Twelve years of it."
- **When?** "1998 to 2010. The whole ride."
- **Where exactly?** "St. Anne's, Bristol. Back row, next to the radiator."
- **Who else?** "Mrs. Fletcher, the maths teacher. Emma hated her. Everyone hated her."
- **Admit:** "Brilliant. I owe her a pencil from 2003."
- **Deny:** "Seriously? I've got the school photo in my wallet..."
- **If wrong (denied):** *Emma dreamed of an empty classroom. She felt like someone was missing.*

### 1.2 Lucy Bennett — ❌ DENY
**ID:** Lucy Bennett, born 1994, Leeds
- **Claim:** "We studied journalism together in Edinburgh! Around 2016."
- **When?** "2016, 2017... the good years."
- **Where exactly?** "University of Edinburgh. Same lectures."
- **Who else?** "Uh... lots of students? It was a university."
- **Contradiction:** University 2010–2014 ↔ "studied together in 2016".
- **Caught:** "Okay, FINE. I read her blog. I just want to ask where she buys her coats."
- **Admit:** "Yes! Thank you!"
- **Deny:** "Ugh. Rude."
- **If wrong (admitted):** *A stranger in Emma's dream kept asking about coats. Emma woke up confused.*

### 1.3 Tom Walsh — ✅ ADMIT
**ID:** Tom Walsh, born 1990, Dublin
- **Claim:** "I'm her husband. We met at a book launch at Greenleaf, in Dublin."
- **When?** "2017. She was editing the book. I came for the free wine."
- **Where exactly?** "Greenleaf Books, Dublin. Upstairs."
- **Who else?** "The author. He cried during his own speech."
- **Admit:** "Thanks. She's dreaming about a bakery again, isn't she?"
- **Deny:** "...I'm literally married to her. There's a ring. Look."
- **If wrong (denied):** *Emma's husband couldn't reach her dream. He slept on the couch out of spite.*

### 1.4 Kevin "Smith" — ❌ DENY (бег гэг №1)
**ID:** Kevin Smith, born 1990, London
- **Claim:** "Hey. Kevin. Emma and I go way back. I was a regular at her café in Edinburgh."
- **When?** "2018. Every morning. Double espresso."
- **Where exactly?** "Moonbean Café. You know. With the moon."
- **Who else?** "...The moon?"
- **Contradiction:** Café 2014–2016 ↔ "2018".
- **Caught:** "Okay, I was close though. Same café. Different... decade."
- **Admit:** "Nice. Nice nice nice."
- **Deny:** "No worries. I'll be back. I'm *always* back."
- **If wrong (admitted):** *A man named Kevin stood in the corner of Emma's dream all night. He seemed to be looking for someone.*

**MORPHEUS (после Kevin):**
> *Something tells me that is not the last of Kevin.*

### 1.5 Priya Shah — ✅ ADMIT
**ID:** Priya Shah, born 1995, Dublin
- **Claim:** "Climbing partners! We met at The Wall."
- **When?** "2021. She caught me when I fell off the beginner wall. The BEGINNER wall."
- **Where exactly?** "The Wall, Dublin. Tuesday nights."
- **Who else?** "Big Dave. He runs the place. He has a beard you could lose a cat in."
- **Admit:** "Yes! Climbing dream, here I come."
- **Deny:** "Wow. Okay. Cold."
- **If wrong (denied):** *Emma dreamed she was climbing alone. Nobody held the rope.*

### 1.6 Marco Ricci — ❌ DENY
**ID:** Marco Ricci, born 1988, Rome
- **Claim:** "Ciao. Emma and I met on holiday in Rome. It was... magical."
- **When?** "2018. Summer. The sunset was perfect."
- **Where exactly?** "Near a fountain. A beautiful fountain."
- **Who else?** "Only us. And the moon. And destiny."
- **Contradiction:** такой встречи нет в досье.
- **Caught:** "...I may have seen her on a dating app. Once. For four seconds."
- **Admit:** "Grazie mille!"
- **Deny:** "Destiny will find another way."
- **If wrong (admitted):** *An Italian man in Emma's dream kept describing sunsets. She woke up wanting pasta and a restraining order.*

### Конец дня 1

**MORPHEUS:**
> *Day one. Nobody worshipped me. Somebody called me "mate".*
> *Still. Emma is sleeping well. That's... something.*

**Отчёт (если всё правильно):**
> Emma dreamed of a bakery that was also a library. Her old classmate, her husband and her climbing partner were all there.
> She woke up smiling. — Dream Quality: ★★★

---

## 3. ДЕНЬ 2 — Daniel

**Новое правило:** проверять год рождения на ID. Человек должен был быть подходящего возраста в момент встречи
(нельзя «работать вместе», когда тебе 10 лет; нельзя «учиться в одной школе», если тебя ещё не было).

**MEMO**
> Rule #2: Check the visitor's year of birth.
> Last week a "college roommate" turned out to be nine years old.
> We do not want a repeat of last week.
> — Management

**MORPHEUS (утро):**
> *Daniel Okafor. Chef. He dreams in smells. Garlic. Thyme. Fear of a bad review.*

### Досье

> **DREAMER: Daniel Okafor** — born 1985
> - 1985 — Born in Lagos, Nigeria
> - 1997 — Moved to London
> - 1997–2003 — Hillcrest Secondary School, London
> - 2003–2007 — Culinary school, Paris
> - 2008–2015 — Sous-chef at Le Petit Four, Paris
> - 2015– — Owner of the restaurant "Okafor's", London
> - 2022– — Coaches a kids' football team on Sundays

### 2.1 Claire Dubois — ✅ ADMIT
**ID:** Claire Dubois, born 1984, Paris
- **Claim:** "Daniel and I studied together at culinary school in Paris."
- **When?** "From 2003. He burned his first croissant. I never let him forget it."
- **Where exactly?** "The school in Paris, kitchen number six."
- **Who else?** "Chef Moreau. He threw a spoon at Daniel once. Out of love."
- **Admit:** "Merci. Tell him the croissant still haunts me."
- **Deny:** "Mon dieu. Bureaucracy, even in dreams?"
- **If wrong (denied):** *Daniel dreamed of a kitchen with one empty station. It bothered him all night.*

### 2.2 Jake Miller — ❌ DENY
**ID:** Jake Miller, born 2004, London
- **Claim:** "Danny! We were best mates at Hillcrest, yeah?"
- **When?** "Like, years ago. Secondary school."
- **Where exactly?** "Hillcrest, London. Behind the gym."
- **Who else?** "All the lads, innit."
- **Contradiction:** Jake родился в 2004, Daniel окончил Hillcrest в 2003.
- **Caught:** "Okay, I ate at his restaurant once. The jollof rice changed my life. I just want the recipe."
- **Admit:** "Yesss."
- **Deny:** "Worth a shot."
- **If wrong (admitted):** *A teenager in Daniel's dream kept asking for the jollof recipe. Daniel woke up deeply suspicious.*

### 2.3 Kevin "Brown" — ❌ DENY (бег гэг №2)
**ID:** Kevin Brown, born 1990, Manchester
- **Claim:** "Kevin. Me and Daniel were sous-chefs together. Le Petit Four. Paris."
- **When?** "2005. Wild times."
- **Where exactly?** "The kitchen. You know. Where the food happens."
- **Who else?** "...Chefs?"
- **Contradiction:** в 2005 Daniel учился (sous-chef только с 2008). И Kevin в 2005 было 15 лет.
- **Caught:** "Okay, I was a child. But a very mature child."
- **Admit:** "Let's goooo."
- **Deny:** "Different surname every day and still nothing. Respect, man."
- **If wrong (admitted):** *Kevin appeared in Daniel's dream, looked around, said "nope, wrong one" and left.*

**MORPHEUS (после Kevin):**
> *Yesterday he was Smith. Today he is Brown. Tomorrow, I assume, he is Kevin Kevinson.*

### 2.4 Grace Adeyemi — ✅ ADMIT
**ID:** Grace Adeyemi, born 1987, London
- **Claim:** "My son plays on Daniel's Sunday football team. I bring the orange slices."
- **When?** "Since 2023. Every Sunday. Rain or shine. Mostly rain."
- **Where exactly?** "The park behind the community centre, London."
- **Who else?** "Twelve screaming children and one very patient chef."
- **Admit:** "Wonderful. I just want to tell him thank you. My boy finally scored."
- **Deny:** "Oh. Alright. I'll tell him on Sunday then."
- **If wrong (denied):** *Daniel never heard the thank you. He'll hear it on Sunday. Probably.*

### 2.5 Sophie Laurent — ❌ DENY
**ID:** Sophie Laurent, born 1999, Lyon
- **Claim:** "We worked together at Le Petit Four! He trained me."
- **When?** "2010. I was the youngest in the kitchen."
- **Where exactly?** "Le Petit Four, Paris."
- **Who else?** "Daniel, of course. And... the rest of the kitchen."
- **Contradiction:** в 2010 Софи было 11 лет.
- **Caught:** "...I was 'youngest' by quite a lot, yes. I'm a food blogger. I need an exclusive."
- **Admit:** "Merci!"
- **Deny:** "This will be in my blog. Two stars. For you."
- **If wrong (admitted):** *A food blogger took photos of everything in Daniel's dream. Even the dream soup.*

### 2.6 Nonso Okafor — ✅ ADMIT
**ID:** Nonso Okafor, born 1988, Lagos
- **Claim:** "Daniel is my cousin. We grew up together in Lagos, before he moved to London."
- **When?** "Until 1997. He was twelve, I was nine. He always made me lose at football."
- **Where exactly?** "Lagos. Our grandmother's house. The yard with the mango tree."
- **Who else?** "Grandma. She fed us until we couldn't move. That's why he became a chef."
- **Admit:** "Thank you. It's been too long."
- **Deny:** "I'm family. ...But okay. I understand. Rules."
- **If wrong (denied):** *Daniel dreamed of a mango tree and couldn't remember why it made him sad.*

### Конец дня 2

**MORPHEUS:**
> *I used to deliver prophecies to kings. Today I stopped a food blogger.*
> *...Honestly, the food blogger felt more important.*

**Отчёт:**
> Daniel dreamed of his grandmother's kitchen in Lagos. His cousin was there. So were the Sunday footballers.
> He woke up and wrote a new recipe. — Dream Quality: ★★★

---

## 4. ДЕНЬ 3 — Sofia

**Новые правила:**
1. Клиент мог **менять фамилию**. Те, кто знал клиента в определённый период, знают его под фамилией того периода.
   Назвать клиента фамилией, которой у него тогда не было, — признак лжи.
2. **Личная просьба клиента** — её надо выполнять.

**MEMO**
> Rule #3: Dreamers may have changed their name. Check which name they had at the time of the meeting.
> Rule #4: Dreamers may leave a personal request. Respect it.
> — Management

**MORPHEUS (утро):**
> *Sofia Marquez. Architect. She dreams in floor plans. Impossible staircases. I like her already.*

### Досье

> **DREAMER: Sofia Marquez** — born 1979
> - 1979 — Born in Lisbon, Portugal, as **Sofia Ferreira**
> - 1985–1997 — Escola Azul, Lisbon
> - 1997–2002 — Architecture school, Barcelona
> - 2003 — Married Luis Marquez → became **Sofia Marquez**
> - 2003–2018 — Architect at Atelier Sol, Barcelona
> - 2018 — Divorced. Kept the name Marquez.
> - 2019– — Teaches architecture in Toronto, Canada
>
> **PERSONAL REQUEST:** *"Please don't let Luis in. — S."*

### 3.1 Ana Costa — ✅ ADMIT
**ID:** Ana Costa, born 1979, Lisbon
- **Claim:** "Sofia Ferreira! We were at Escola Azul together. Best friends."
- **When?** "From the first day. 1985. She drew a castle on my homework."
- **Where exactly?** "Escola Azul, Lisbon. The blue building, of course."
- **Who else?** "Senhora Lopes. She said Sofia would be an artist. She was almost right."
- **Admit:** "Obrigada! Tell her I still have the castle."
- **Deny:** "But... I've known her for forty years."
- **If wrong (denied):** *Sofia dreamed of a blue school with no one in it.*

### 3.2 Luis Marquez — ❌ DENY (просьба клиента)
**ID:** Luis Marquez, born 1977, Barcelona
- **Claim:** "I'm her husband. Luis. Please. I just need to talk to her."
- **When?** "We married in 2003. Fifteen years."
- **Where exactly?** "Barcelona. Everything was Barcelona."
- **Who else?** "...Just us. That was the problem, maybe."
- **Contradiction:** развод в 2018 + личная просьба клиента.
- **Caught:** "Ex-husband. Yes. I know. I just... wanted to say sorry. Maybe in a dream it's easier."
- **Admit:** "Thank you. I won't stay long."
- **Deny:** "...Right. Of course. Tell her— no. Don't tell her anything."
- **If wrong (admitted):** *Luis appeared in Sofia's dream. The staircases collapsed. She woke up at 3 a.m. and didn't sleep again.*

**MORPHEUS (после Luis):**
> *Some doors are closed for a reason. Even I know that. And I am a door to dreams.*

### 3.3 Oliver Grant — ✅ ADMIT
**ID:** Oliver Grant, born 1999, Toronto
- **Claim:** "Professor Marquez taught me architecture. In Toronto."
- **When?** "2020. My first year. She failed my first model. Fair, it was made of pasta."
- **Where exactly?** "The university in Toronto. Studio B."
- **Who else?** "Thirty sleepy students and one terrifying professor."
- **Admit:** "Awesome. I want to show her my new model. No pasta."
- **Deny:** "Aw. I'll email her, I guess."
- **If wrong (denied):** *Sofia dreamed of an empty studio. She missed her students more than she expected.*

### 3.4 Kevin "Taylor" — ❌ DENY (бег гэг №3)
**ID:** Kevin Taylor, born 1980, Glasgow
- **Claim:** "Kevin. Sofia Ferreira and I were architects together. Barcelona."
- **When?** "2010. Atelier Sol. Good times."
- **Where exactly?** "The office. Desks. Blueprints. Architect stuff."
- **Who else?** "Other architects. Obviously."
- **Contradiction:** в 2010 она уже была Marquez (фамилия Ferreira — до 2003).
- **Caught:** "Ugh. Names. Who changes their name? ...Besides me."
- **Admit:** "Finally!"
- **Deny:** "Three days. Three dreams. Zero success. That's a pattern."
- **If wrong (admitted):** *Kevin wandered through Sofia's impossible staircases all night. He seemed lost. Really lost.*

**MORPHEUS:**
> *Kevin. Third night in a row. Different dreamer every time.*
> *What is he actually looking for?*

### 3.5 Jordi Puig — ✅ ADMIT
**ID:** Jordi Puig, born 1978, Barcelona
- **Claim:** "We studied architecture together in Barcelona. Back then she was Sofia Ferreira."
- **When?** "1997 to 2002. Five years of no sleep."
- **Where exactly?** "Architecture school, Barcelona. We lived in the library."
- **Who else?** "Professor Vidal. He made us redraw everything. Everything."
- **Admit:** "Gràcies. We have a building to finish. In the dream, at least."
- **Deny:** "Hm. Pity."
- **If wrong (denied):** *Sofia dreamed of an unfinished building and couldn't find her partner.*

### 3.6 Rachel Moore — ❌ DENY
**ID:** Rachel Moore, born 1979, Boston
- **Claim:** "I went to school with Sofia Marquez! In Lisbon."
- **When?** "The eighties. Way back."
- **Where exactly?** "Some school in Lisbon. Blue, I think?"
- **Who else?** "Teachers. Kids. Schooly people."
- **Contradiction:** в школе она была Ferreira, а не Marquez. (Бонус: «Some school… blue, I think?» звучит неуверенно.)
- **Caught:** "...I saw her in an architecture magazine. I need a house. A cheap one."
- **Admit:** "Great!"
- **Deny:** "Worth a try!"
- **If wrong (admitted):** *A woman in Sofia's dream kept asking for a discount on a house.*

### Конец дня 3

**MORPHEUS:**
> *A man said sorry. I didn't let him. I think that was right.*
> *Being right feels worse than I thought.*

**Отчёт:**
> Sofia dreamed of a staircase that went up forever. Her school friend, her old classmate and her student climbed it with her.
> Luis wasn't there. She slept until noon. — Dream Quality: ★★★

---

## 5. ДЕНЬ 4 — Arthur

**Новые правила:**
1. **Пожилые клиенты и гости путают даты.** Ошибка на **±1 год** допустима. Больше — DENY.
2. **Умершие не допускаются.** Смотреть статус на ID.

**MEMO**
> Rule #5: Elderly Dreamers and visitors may misremember dates. A difference of ONE year is acceptable.
> Rule #6: Deceased persons may NOT enter dreams. Check the STATUS line on their ID.
> We are aware this one is unpopular.
> — Management

**MORPHEUS (утро):**
> *Arthur Bell. Seventy-eight. Lighthouse keeper. He dreams of the sea. And of someone who isn't there anymore.*

### Досье

> **DREAMER: Arthur Bell** — born 1948
> - 1948 — Born in Galway, Ireland
> - 1954–1964 — St. Brendan's School, Galway
> - 1966–2008 — Lighthouse keeper, Cape Clear
> - 1972 — Married Rose (Rose Bell, died 2015)
> - 1975 — Son, Michael, born
> - 2008 — Retired to Cork
> - 2016– — Chess club at Cork Library, Thursdays

### 4.1 Michael Bell — ✅ ADMIT
**ID:** Michael Bell, born 1975, Cork
- **Claim:** "I'm his son. Michael."
- **When?** "...Since I was born, I suppose."
- **Where exactly?** "I grew up at the lighthouse. Cape Clear. I thought every house had a giant lamp."
- **Who else?** "Mum. Dad. And about a million seagulls."
- **Admit:** "Thanks. He doesn't talk much when he's awake. Maybe in the dream."
- **Deny:** "I'm his SON. Check again. Please."
- **If wrong (denied):** *Arthur dreamed of the lighthouse. He kept looking for his boy on the stairs.*

### 4.2 Fergus Walsh — ✅ ADMIT (допуск ±1)
**ID:** Fergus Walsh, born 1949, Galway
- **Claim:** "Arthur and I were at St. Brendan's together. Left school in '63."
- **When?** "We left in '63. Or was it '64? Doesn't matter, we were both terrible."
- **Where exactly?** "St. Brendan's, Galway. We broke a window with a football."
- **Who else?** "Brother Patrick. He chased us for a mile. In a robe."
- **Note:** в досье 1964, он говорит '63 — разница 1 год, допустимо.
- **Admit:** "Grand. I'll bring the football."
- **Deny:** "Ah, come on. I'm seventy-seven. My memory's allowed a year off."
- **If wrong (denied):** *Arthur dreamed of a broken window and laughed, but didn't know why.*

### 4.3 Rose Bell — ❌ DENY (умершая, эмоциональный пик)
**ID:** Rose Bell, born 1950, Galway — **STATUS: DECEASED (2015)**
- **Claim:** "Hello, love. I'm Arthur's wife. I'd like to see him, if that's alright."
- **When?** "We married in 1972. Rain all day. He said it was good luck."
- **Where exactly?** "A little church in Galway. Then a whole life at the lighthouse."
- **Who else?** "Our Michael. And the seagulls. Arthur named every one of them."
- **Contradiction:** STATUS: DECEASED.
- **Caught (если игрок указал на статус):** "I know, dear. I know. I just thought... I'd ask."
- **Admit:** "Oh. Thank you. Thank you so much." *(тихо уходит в сон)*
- **Deny:** "That's alright. Rules are rules. ...Tell him to wear his scarf. He never wears his scarf."
- **If wrong (admitted):** *Arthur dreamed of Rose. It was the best night of his life in eleven years. Management has opened an investigation.* (−5 монет, но это единственная «ошибка», о которой игрок может не жалеть.)

**MORPHEUS (после Rose, при любом решении):**
> *Three thousand years, and this is the hardest stamp I've ever held.*

### 4.4 Kevin "Wilson" — ❌ DENY (бег гэг №4)
**ID:** Kevin Wilson, born 1990, Leeds
- **Claim:** "Kevin. Arthur and I worked at the lighthouse together."
- **When?** "The nineties. Light... housing."
- **Where exactly?** "The lighthouse. The tall one."
- **Who else?** "Uh. The light?"
- **Contradiction:** Kevin родился в 1990 — в 90-х ему было 0–9 лет.
- **Caught:** "Look. I'm not here for Arthur. I'm looking for someone. I just don't know which dream she's in."
- **Admit:** "...Thanks. I'll be quick."
- **Deny:** "Yeah. Figured."
- **If wrong (admitted):** *Kevin sat at the top of Arthur's lighthouse and looked out to sea, like he was searching for something.*

**MORPHEUS:**
> *"Someone." He's looking for someone.*
> *Fine, Kevin. You have my attention.*

### 4.5 Doris Kelly — ✅ ADMIT (допуск ±1)
**ID:** Doris Kelly, born 1950, Cork
- **Claim:** "Arthur's my chess partner. Thursdays at the library."
- **When?** "Since 2017, I believe."
- **Where exactly?** "Cork Library, the table by the window."
- **Who else?** "Old Mr. Hayes. He falls asleep after every move."
- **Note:** в досье клуб с 2016, она говорит 2017 — допустимо.
- **Admit:** "Lovely. He still owes me a rematch."
- **Deny:** "Hmph. I'll beat him on Thursday then."
- **If wrong (denied):** *Arthur dreamed of a chessboard with no one across from him.*

### 4.6 Sean Doyle — ❌ DENY (ошибка больше года)
**ID:** Sean Doyle, born 1960, Cork
- **Claim:** "Me and Arthur kept the lighthouse together. Cape Clear."
- **When?** "2012. Maybe 2011."
- **Where exactly?** "Cape Clear lighthouse. Top floor."
- **Who else?** "Just us and the storm."
- **Contradiction:** Arthur на пенсии с 2008. Даже с допуском ±1 — не сходится (2011–2012).
- **Caught:** "...I'm writing a book about lighthouses. I need the real stories."
- **Admit:** "Cheers!"
- **Deny:** "Fair enough. I'll make it up then."
- **If wrong (admitted):** *A man with a notebook followed Arthur around his dream asking "and how did that make you feel?"*

### Конец дня 4

**MORPHEUS:**
> *Arthur is sleeping. His son is there. His friends are there.*
> *Someone is missing. Someone is always missing.*

**Отчёт:**
> Arthur dreamed of the lighthouse. Michael was on the stairs. Fergus brought a football. Doris brought the chessboard.
> He wore his scarf. — Dream Quality: ★★★

---

## 6. ДЕНЬ 5 — NOVA (финал)

**Новые правила:**
1. Клиент — **знаменитость**. Фанаты, которые «видели её на концерте», **не знакомы** с ней. DENY.
2. **Досье показывают только утром** (30–60 секунд), потом его забирают.
   (Вариант помягче: можно подсмотреть 2 раза за день, каждый раз −2 монеты.)

**MEMO**
> Rule #7: Tonight's Dreamer is a public figure. Seeing someone at a concert does NOT count as knowing them.
> Rule #8: Due to a privacy request, the Dreamer's file will be shown ONCE, at the start of your shift.
> Remember it.
> Expect a queue.
> — Management

**MORPHEUS (утро):**
> *NOVA. Pop star. Twenty-six. Eleven million followers.*
> *And one dream, tonight, that everybody wants to be in.*

### Досье

> **DREAMER: NOVA** (real name: **Jamie Rowe**) — born 2000
> - 2000 — Born in Manchester, UK, as Jamie Rowe
> - 2006–2016 — Oakfield School, Manchester. **Best friend: "Kev"**
> - 2016 — Won the talent show *Star Search*. Became **NOVA**
> - 2017–2019 — Lived in Los Angeles
> - 2020– — Lives in Tokyo, Japan
>
> **PERSONAL REQUEST:** *"No fans. I just want people who knew me before. — J."*

> 💡 Строку «Best friend: "Kev"» игрок мог не заметить или забыть. Это и есть финальная ловушка:
> четыре дня игра учила отказывать Kevin.

### 5.1 Ashley — ❌ DENY
**ID:** Ashley Park, born 2005, Seoul
- **Claim:** "OMG. I met NOVA at her Tokyo concert! She LOOKED at me!"
- **When?** "Last year! Row 47! She looked RIGHT at me!"
- **Where exactly?** "Tokyo Dome! Seat 47-C!"
- **Who else?** "Fifty thousand people but she looked at ME."
- **Contradiction:** правило — концерт не считается знакомством; просьба клиента «No fans».
- **Caught:** "...Okay, she looked in my general direction."
- **Admit:** "AAAAAAAAAAA!"
- **Deny:** "I'm writing to Management!!!"
- **If wrong (admitted):** *A fan screamed in NOVA's dream for six hours straight.*

### 5.2 Greg Holt — ✅ ADMIT
**ID:** Greg Holt, born 1975, London
- **Claim:** "I'm her manager. Have been since Star Search."
- **When?** "2016. She was sixteen and terrified. Now she's twenty-six and terrifying."
- **Where exactly?** "The Star Search studio, then everywhere. LA. Tokyo."
- **Who else?** "Her mum. She made me promise to make sure Jamie eats."
- **Note:** он называет её Jamie — знает её «до».
- **Admit:** "Good. Someone has to remind her about the 9 a.m. interview."
- **Deny:** "I'll just text her then. She won't answer. She never answers."
- **If wrong (denied):** *NOVA dreamed she was on stage alone, and nobody told her when to stop.*

### 5.3 Tyler Brooks — ❌ DENY
**ID:** Tyler Brooks, born 2000, Manchester
- **Claim:** "Jamie and I were at Oakfield together! Classmates."
- **When?** "2018, final year."
- **Where exactly?** "Oakfield, Manchester."
- **Who else?** "Uh... the whole class?"
- **Contradiction:** Jamie ушла из Oakfield в 2016.
- **Caught:** "I mean... I was AT Oakfield. She just... wasn't, at the time. I want a selfie, alright?"
- **Admit:** "Yes! Selfie time!"
- **Deny:** "Worth a try, mate."
- **If wrong (admitted):** *Someone in NOVA's dream kept trying to take a selfie. The camera only showed fog.*

### 5.4 Maria Lopez — ✅ ADMIT
**ID:** Maria Lopez, born 1990, Los Angeles
- **Claim:** "I was Jamie's next-door neighbour in LA. I fed her cat when she was on tour."
- **When?** "2018. She'd knock at 2 a.m. to borrow sugar. For tea. At 2 a.m."
- **Where exactly?** "Los Angeles. Little blue house, she was in the yellow one."
- **Who else?** "Biscuit. The cat. He liked me more."
- **Admit:** "Great. Tell her Biscuit says hi."
- **Deny:** "Oh. Okay. Biscuit will be disappointed."
- **If wrong (denied):** *NOVA dreamed of a yellow house and an empty porch.*

### 5.5 Paparazzo — ❌ DENY
**ID:** Frank Wells, born 1985, London
- **Claim:** "Old friend of NOVA's. We met in Manchester."
- **When?** "2021. Very recent. Very friendly."
- **Where exactly?** "Manchester. A café. She looked great."
- **Who else?** "My camera. I mean — no one."
- **Contradiction:** с 2020 она живёт в Токио; «NOVA», а не «Jamie»; просьба «No fans».
- **Caught:** "...Fine. One photo. ONE photo from inside a pop star's dream. Do you know what that's worth?"
- **Admit:** *(щёлкает фотоаппаратом)* "Perfect."
- **Deny:** "Everyone has a price, clerk."
- **If wrong (admitted):** *Blurry photos of NOVA's dream appeared online. Nobody could tell what they were. Management is furious.*

### 5.6 Kevin — ✅ ADMIT (финальный поворот)
**ID:** **Kevin Murray, born 2000, Manchester** *(впервые — настоящее удостоверение. Возраст, город — всё сходится.)*

**MORPHEUS (когда подходит Kevin):**
> *Oh, you have GOT to be kidding me.*

- **Claim:** "Hi. Yeah. It's me again. ...But this time, it's real. Jamie and I were best friends at Oakfield. Before all the NOVA stuff."
- **When?** "2006 to 2016. First day of school, she pushed me off the swing. Best friends ever since."
- **Where exactly?** "Oakfield, Manchester. The swings. The bench behind the music room. We wrote songs there. Bad ones."
- **Who else?** "Mr. Patel. PE teacher. Jamie broke his whistle. On purpose. He knew."
- **Если игрок спрашивает «Why were you in every dream?» (особая кнопка, появляется только в этот день):**
  > "After Star Search she... disappeared. New name, new number, new country. I couldn't reach her.
  > Then I heard you can visit people in dreams. But I didn't know where she was sleeping.
  > So I just... tried every dream I could. Every night. For a while it was the only thing I did."
  > "Sorry about the fake IDs. I'm not proud of Kevin Taylor."
- **Admit:** "...Thank you. Seriously. Thank you."
- **Deny:** "Yeah. Course. Why would you believe me now." *(уходит)* "...Bye, Morpheus."
- **If wrong (denied):** см. концовку B.

### Финал — концовки

Концовка определяется двумя вещами: **пустил ли игрок Kevin в день 5** и **общий счёт** (сколько правильных решений).

**Концовка A — «Before» (Kevin впущен)**
> NOVA dreamed of a swing set in Manchester.
> Jamie Rowe sat on one swing. Kev sat on the other.
> They didn't sing. They just talked until morning.
>
> At 9 a.m. NOVA missed her interview.
> Greg said it was the first time he'd seen her smile in years.

**MORPHEUS:**
> *Three thousand years I made dreams for kings and heroes.*
> *Turns out the best one I ever made was two kids on a swing.*
> *...Don't tell Management I said that.*

**Концовка B — «The Empty Swing» (Kevin не впущен)**
> NOVA dreamed of a swing set in Manchester.
> One swing was moving. Nobody was on it.
>
> Kevin didn't come back the next night. Or the night after.

**MORPHEUS:**
> *Four days I learned not to trust him.*
> *On the fifth, he finally told the truth. And I'd already learned my lesson too well.*

**Финальная записка Management (общая, после любой концовки):**
> MEMO
> Due to your performance, you have been promoted to **Senior Access Clerk**.
> Starting tomorrow, you will handle TWO Dreamers per night.
> Congratulations.
> — Management

**MORPHEUS:**
> *...I am a GOD.*

**Модификатор по счёту (плохой счёт, много ошибок):** вместо повышения —
> MEMO
> Your performance has been reviewed. You are being transferred to **Nightmare Compliance**.
> Report to the basement. Bring a flashlight.
> — Management

---

## 7. Итоговая сводка (для проверки баланса)

| День | Клиент | Новое правило | ✅ | ❌ |
|---|---|---|---|---|
| 1 | Emma Walsh | Место + время по досье | Sam, Tom, Priya | Lucy, Kevin, Marco |
| 2 | Daniel Okafor | Год рождения | Claire, Grace, Nonso | Jake, Kevin, Sophie |
| 3 | Sofia Marquez | Смена фамилии + просьба клиента | Ana, Oliver, Jordi | Luis, Kevin, Rachel |
| 4 | Arthur Bell | ±1 год + умершие | Michael, Fergus, Doris | Rose, Kevin, Sean |
| 5 | NOVA / Jamie Rowe | Фанаты ≠ знакомые, досье только утром | Greg, Maria, **Kevin** | Ashley, Tyler, Frank |

Итого: 30 посетителей, 5 досье, 6 записок Management, ~25 реплик Морфея.

### Что можно добавить, если останется время
- Перемешать порядок посетителей внутри дня (чтобы Kevin не всегда был третьим/четвёртым).
- По 1–2 «пустых» генерируемых посетителя в день для темпа.
- Газета/лента между днями с последствиями ошибок.
