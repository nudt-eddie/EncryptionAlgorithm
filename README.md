# 加密算法实现项目

这个项目包含了多种常见加密算法的Python实现。这些实现主要用于学习目的，展示了各种加密技术的基本原理。

## 项目结构
Algorithm/
├── Asymmetric/
│ ├── DSA.py
│ ├── ECC.py
│ └── RSA.py
├── Hash/
│ ├── MD5.py
│ ├── SHA1.py
│ ├── SHA2.py
│ └── SHA3.py
├── Hybrid/
│ └── ECIES.py
├── MAC/
│ ├── CMAC.py
│ └── HMAC.py
├── Substitution/
│ ├── Atbash.py
│ ├── Caesar.py
│ ├── Playfair.py
│ └── Vigenere.py
└── Symmetric/
├── 3DES.py
├── AES.py
├── DES.py
└── RC4.py

## 已实现的算法

### 非对称加密
- DSA (Digital Signature Algorithm)
- ECC (Elliptic Curve Cryptography)
- RSA (Rivest–Shamir–Adleman)

### 哈希函数
- MD5
- SHA-1
- SHA-2 (SHA-256, SHA-512)
- SHA-3 (Keccak)

### 混合加密
- ECIES (Elliptic Curve Integrated Encryption Scheme)
- RSA_OAEP(RSA with Optimal Asymmetric Encryption Padding)

### 消息认证码
- CMAC (Cipher-based Message Authentication Code)
- HMAC (Hash-based Message Authentication Code)

### 替换密码
- Atbash 密码
- 凯撒密码
- Playfair 密码
- 维吉尼亚密码

### 对称加密
- 3DES (Triple DES)
- AES (Advanced Encryption Standard)
- DES (Data Encryption Standard)
- RC4

### 量子加密
- 量子密钥分发

### 其他
- 椭圆曲线加密
- 数字签名

## 使用说明

每个算法文件都包含了示例使用代码。您可以直接运行这些Python文件来查看算法的工作原理。

例如，要运行AES加密算法：


