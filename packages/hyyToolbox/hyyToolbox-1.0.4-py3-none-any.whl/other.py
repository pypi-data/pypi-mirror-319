"""导入模块"""
try:
    from cryptography.fernet import Fernet

except ImportError:

    import pip
    pip.main(["install", "--user", "cryptography"])

    from cryptography.fernet import Fernet

#加密文件
def Encryption(Encrypt_files,key_name,Save_name):
    # 生成密钥
    key = Fernet.generate_key()

    # 保存密钥到文件
    with open(f'{key_name}.key', 'wb') as key_file:
        key_file.write(key)

    print("密钥已生成并保存")

    from cryptography.fernet import Fernet

    # 读取密钥
    with open(f'{key_name}.key', 'rb') as key_file:
        key = key_file.read()

    # 初始化加密器
    cipher = Fernet(key)


    # 加密文件
    with open(Encrypt_files, 'rb') as file:
        file_data = file.read()

    # 加密内容
    encrypted_data = cipher.encrypt(file_data)

    # 将加密后的内容写入新文件
    with open(Save_name, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

    print("文件已加密")

#解密文件
def decrypt(Encrypt_files,key_name,Save_name):
    # 读取密钥
    with open(f'{key_name}.key', 'rb') as key_file:
        key = key_file.read()

    # 初始化解密器
    cipher = Fernet(key)

    # 读取加密文件
    with open(Encrypt_files, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    # 解密内容
    decrypted_data = cipher.decrypt(encrypted_data)

    # 将解密后的内容写入新文件
    with open(Save_name, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

    print("文件已解密")