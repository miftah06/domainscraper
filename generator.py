import random
import string

def generate_random_subdomains(num_subdomains):
    subdomains = []
    for _ in range(num_subdomains):
        subdomain_length = random.randint(1, 5)  # Ganti batasan panjang subdomain sesuai kebutuhan
        subdomain = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(subdomain_length))
        subdomains.append(subdomain)
    return subdomains

def save_to_file(subdomains, file_path="domain.txt"):
    with open(file_path, 'w') as file:
        for subdomain in subdomains:
            domain = f"{subdomain}"  # Ganti dengan ekstensi domain yang diinginkan
            file.write(f"{domain}\n")

if __name__ == "__main__":
    num_subdomains = 10  # Ganti dengan jumlah subdomain yang diinginkan
    subdomains = generate_random_subdomains(num_subdomains)
    save_to_file(subdomains)
    print(f"{num_subdomains} subdomains telah disimpan dalam domain.txt")
