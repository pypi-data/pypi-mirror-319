from pwn import *

def main():
    p = process('/flag')
    eq = p.recvuntil(b" =")
    eq = eq[:-2]
    eq = eq.decode()
    p.recvuntil(b" ?\n")
    p.sendline(str(eval(eq)))
    print(p.recvall().decode())

if __name__ == "__main__":
    main()
