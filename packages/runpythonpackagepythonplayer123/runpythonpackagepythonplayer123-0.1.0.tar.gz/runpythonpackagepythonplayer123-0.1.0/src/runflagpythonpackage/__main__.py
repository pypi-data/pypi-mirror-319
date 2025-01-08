import subprocess

def main():
    print(subprocess.run(["/flag"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8"))

if __name__ == "__main__":
    main()
