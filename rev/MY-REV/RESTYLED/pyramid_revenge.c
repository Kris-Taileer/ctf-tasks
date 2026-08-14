#define _GNU_SOURCE
#include <stdio.h>
#include <math.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdint.h>

#define W 80
#define H 26
#define FLAGLEN 46

static const char GRAD[] = " .,:;+=*xoO#%@$";
static const int  WARM[11] = { 52, 88, 124, 130, 136, 166,
                               172, 208, 214, 220, 226 };

static uint8_t S1[256];
static uint8_t S2[256];
static uint8_t KS[FLAGLEN];

static void build_sbox(uint64_t seed, uint8_t *out)
{
    uint64_t state = seed;
    for (int i = 0; i < 256; i++) out[i] = (uint8_t)i;
    for (int i = 255; i > 0; i--) {
        state = state * 1664525ULL + 1013904223ULL;
        uint32_t r = (uint32_t)(state >> 16);
        int j = (int)(r % (uint32_t)(i + 1));
        uint8_t t = out[i]; out[i] = out[j]; out[j] = t;
    }
}

static uint32_t f32_bits(float v)
{
    union { float f; uint32_t u; } c;
    c.f = v;
    return c.u;
}

static void build_keystream(void)
{
    const float phi_conj = 0.6180339887f;
    const float r = 3.99f;
    float x = phi_conj;
    for (int i = 0; i < FLAGLEN; i++) {
        KS[i] = (uint8_t)(f32_bits(x) & 0xFFu);
        float one_minus_x = 1.0f - x;
        float rx = r * x;
        x = rx * one_minus_x;
    }
}

static const uint8_t ENC[FLAGLEN] = {
    0x8d,0x28,0xa2,0xe2,0x60,0xdc,0xa9,0xbf,0x42,0xdd,0x09,
    0x6f,0x1d,0x01,0x8c,0x5e,0x47,0xc1,0x06,0xe5,0x8d,0x7b,
    0x52,0x1a,0x8d,0xb1,0x1d,0x7f,0x3d,0xb2,0x6b,0x51,0x1f,
    0x83,0x7c,0xa2,0x47,0xb6,0x4d,0x74,0x09,0x32,0x00,0xd9,
    0x00,0xee
};
static const uint8_t KEY[4] = { 0xcc, 0x99, 0x8c, 0xbf };

static char  scr[W * H];
static float zb [W * H];
static int   cb [W * H];

typedef struct { float x, y, z; } V3;

static void cleanup(int sig)
{
    (void)sig;
    puts("\x1b[?25h\x1b[0m");
    exit(0);
}

static void draw_face(V3 a, V3 b, V3 c)
{
    float ux = b.x - a.x, uy = b.y - a.y, uz = b.z - a.z;
    float vx = c.x - a.x, vy = c.y - a.y, vz = c.z - a.z;

    float nx = uy * vz - uz * vy;
    float ny = uz * vx - ux * vz;
    float nz = ux * vy - uy * vx;

    float len = sqrtf(nx * nx + ny * ny + nz * nz);
    if (len > 1e-7f) { nx /= len; ny /= len; nz /= len; }

    float za = a.z + 5.5f, zbb = b.z + 5.5f, zc = c.z + 5.5f;
    if (za < 0.1f || zbb < 0.1f || zc < 0.1f) return;

    int xa = (int)(a.x / za * 30.0f + 40.0f);
    int ya = (int)(-a.y / za * 15.0f + 13.0f);
    int xb = (int)(b.x / zbb * 30.0f + 40.0f);
    int yb = (int)(-b.y / zbb * 15.0f + 13.0f);
    int xc = (int)(c.x / zc * 30.0f + 40.0f);
    int yc = (int)(-c.y / zc * 15.0f + 13.0f);

    int minx = xa < xb ? xa : xb; if (xc < minx) minx = xc;
    int maxx = xa > xb ? xa : xb; if (xc > maxx) maxx = xc;
    int miny = ya < yb ? ya : yb; if (yc < miny) miny = yc;
    int maxy = ya > yb ? ya : yb; if (yc > maxy) maxy = yc;
    if (minx < 0) minx = 0;
    if (maxx > W - 1) maxx = W - 1;
    if (miny < 0) miny = 0;
    if (maxy > H - 1) maxy = H - 1;
    if (maxx < minx || miny > maxy) return;

    float area = (float)((ya - yc) * (xc - xb) + (xa - xc) * (yb - yc));
    if (fabsf(area) < 0.5f) return;

    float lum = nx * 0.608f + ny * 0.76f + nz * -0.243f;
    if (lum < 0.1f) lum = 0.1f;

    int gi = (int)(lum * 14.0f); if (gi > 14) gi = 14;
    int ci = (int)(lum * 10.0f); if (ci > 10) ci = 10;
    char ch = GRAD[gi];
    int  col = WARM[ci];

    for (int y = miny; y <= maxy; y++) {
        for (int x = minx; x <= maxx; x++) {
            int w0 = (yb - yc) * (x - xc) + (xc - xb) * (y - yc);
            int w1 = (yc - ya) * (x - xc) + (xa - xc) * (y - yc);
            float l0 = (float)w0 / area; if (l0 < 0.0f) continue;
            float l1 = (float)w1 / area; if (l1 < 0.0f) continue;
            float l2 = 1.0f - l0 - l1;   if (l2 < 0.0f) continue;

            float z = l0 * za + l1 * zbb + l2 * zc;
            int idx = y * W + x;
            if (zb[idx] > z) {
                zb[idx]  = z;
                scr[idx] = ch;
                cb[idx]  = col;
            }
        }
    }
}

static int check(const char *s)
{
    if (strlen(s) != FLAGLEN) return 0;
    uint8_t prev = 0;
    for (int i = 0; i < FLAGLEN; i++) {
        uint8_t a = (uint8_t)s[i] ^ prev;
        uint8_t b = S1[a];
        uint8_t c = b ^ KS[i];
        uint8_t d = S2[c];
        uint8_t e = d ^ KEY[i & 3];
        if (e != ENC[i]) return 0;
        prev = (uint8_t)s[i];
    }
    return 1;
}

int main(int argc, char **argv)
{
    const float phi = 1.6180339887f;
    uint32_t seed2 = f32_bits(phi);
    build_sbox(0x4b657931ULL, S1);
    build_sbox((uint64_t)seed2, S2);
    build_keystream();

    if (argc > 1) {
        if (check(argv[1]))
            puts("\x1b[32mCORRECT! The pyramid remembers everything now.\x1b[0m");
        else
            puts("\x1b[31mWRONG. The chain is broken.\x1b[0m");
        return 0;
    }

    signal(SIGINT,  cleanup);
    signal(SIGTERM, cleanup);
    printf("\x1b[2J\x1b[?25l");

    float a = 0.0f;
    for (;;) {
        for (int i = 0; i < W * H; i++) { scr[i] = ' '; zb[i] = 1e9f; cb[i] = -1; }

        float sa, ca, sb, cbb;
        sincosf(a, &sa, &ca);
        float b = sinf(a * 0.4f) * 0.05f + 0.32f;
        sincosf(b, &sb, &cbb);

        static const V3 P[5] = {
            {  0.0f,  1.7f,  0.0f },
            {  1.1f, -0.5f, -1.1f },
            { -1.1f, -0.5f, -1.1f },
            { -1.1f, -0.5f,  1.1f },
            {  1.1f, -0.5f,  1.1f },
        };
        V3 v[5];
        for (int i = 0; i < 5; i++) {
            float x1 = P[i].z * sa - P[i].x * ca;
            float z1 = P[i].x * sa + P[i].z * ca;
            v[i].x = x1;
            v[i].y = P[i].y * cbb - z1 * sb;
            v[i].z = P[i].y * sb  + z1 * cbb;
        }

        draw_face(v[0], v[2], v[1]);
        draw_face(v[0], v[3], v[2]);
        draw_face(v[0], v[4], v[3]);
        draw_face(v[0], v[1], v[4]);
        draw_face(v[1], v[2], v[4]);
        draw_face(v[2], v[3], v[4]);

        printf("\x1b[H");
        printf("\x1b[38;5;214m%*s~~~THE PYRAMID REMEMBERS ~~~\x1b[0m\n\n", 28, "");

        int last = -2;
        for (int y = 0; y < H; y++) {
            for (int x = 0; x < W; x++) {
                int c = cb[y * W + x];
                if (c != last) {
                    if (c >= 0) printf("\x1b[38;5;%dm", c);
                    else        printf("\x1b[0m");
                    last = c;
                }
                putc(scr[y * W + x], stdout);
            }
            putc('\n', stdout);
        }
        printf("\x1b[0m");
        fflush(stdout);
        usleep(33333);
        a += 0.04f;
    }
}
