#STOLOVAYA TASK GUYS#
```
Меню:
  1) Булочка ............ 10 монет
  2) Сок ................ 15 монет
  3) Секретный пирожок .. 1000 монет  (только для своих)
  0) Выход

[баланс: 50] выберите товар (0-3)> 3
Сколько штук "Секретный пирожок"? > -1
Не хватает монет!
[баланс: 50] выберите товар (0-3)>
```

actually it's a pwn in one mathematical equation:

1000 * x <= 50 mod 2^32

it comes from assembly listing of the task:

<img width="1920" height="1080" alt="photo_2026-11-16_02-15-09" src="https://github.com/user-attachments/assets/90d8ef0f-a813-4e5c-99e7-3b6a5263e223" />

there're exact instructions that makes the hole in logic (not really but you'll get everything soon)

also in this exact moment program flow asks you to put some data (actually no bufs in this binary are pwnable enough for overflow or rop or smth, so watch my hands)

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9b80eccb-39fe-428f-a633-16ae88bb8274" />

u see, it wants unsigned int from us as a number of pies we want to buy...(we need to buy a secret one okay), and makes everything possible
in instruction it looks like:

```asm
.text:00000000000011D0                 lea     rsi, [rsp+48h+var_3C]
.text:00000000000011D5                 lea     rdi, aU         ; "%u"  //better to be %d uk uk
.text:00000000000011DC                 call    ___isoc99_scanf
.text:00000000000011E1                 cmp     eax, 1
.text:00000000000011E4                 jnz     loc_1291                // checks that we got it a number and not the shit
.text:00000000000011EA                 mov     edx, [rsp+48h+var_3C]   // moves our input to edx
.text:00000000000011EE                 test    edx, edx
.text:00000000000011F0                 jz      loc_1280               // checks that we wanna buy at least one
.text:00000000000011F6                 mov     ecx, r12d              // r12d contains 1000 (price of the secret pie)
.text:00000000000011F9                 imul    ecx, edx               // does: our input * 1000
.text:00000000000011FC                 cmp     ebp, ecx               // ebp contains our money (50 basically)
.text:00000000000011FE                 jb      short loc_1268         // next program flow
```
So the task can be pwned by the logic of we want to multiply 1000 to smth that turns the sum we need to pay less than what we have in our pocket

we came to this equation:  "1000 * x <= 50 mod 2^32"  mod 2^32 cuz the variable contains int signed,
but our exploitation depends exactly on that we can enter the unsigned int value and it will be multiplied with signed int that will be later compared with 50

my next step was just

<img width="820" height="795" alt="image" src="https://github.com/user-attachments/assets/0f3d9720-15ad-419b-94bd-fb34239f52e7" />

yes, i fuckin love wolfram, and it gives us real stuff (actually there were no solutions for =50 and =49 so u need to bruteforce a little)

so we take 158913790 from "x congruent 158913790 (mod 536870912)"
and it's one of nums that will give us flag

```bash
kris@bigfuckingputer ~/D/L/innoOPEN [127]> ./stolovaya 
=== Школьный автомат-буфет ===
На подарочной карте: 50 монет.
Меню:
  1) Булочка ............ 10 монет
  2) Сок ................ 15 монет
  3) Секретный пирожок .. 1000 монет  (только для своих)
  0) Выход

[баланс: 50] выберите товар (0-3)> 3
Сколько штук "Секретный пирожок"? > 158913790
Выдано: Секретный пирожок x158913790. Списано 48 монет.
Держите секретный пирожок, внутри записка: CTF{FAKE_FLAG_NOT_SOLVE_IT}
kris@bigfuckingputer ~/D/L/innoOPEN> 
```

That's the task, and, there're some bonus materials: (im explaining everything right on one photo after ctf to my friend)
<img width="1080" height="1920" alt="image" src="https://github.com/user-attachments/assets/ebd203ef-97cc-400a-9f88-721a6dd97c10" />
