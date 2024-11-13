from pyppeteer_stealth import stealth
from pyppeteer import launch
from bs4 import BeautifulSoup
import json
import asyncio
import signal
import sys
import time
import os

SUBMISSION_IDS_FILE = './sample_data/submission_ids_and_handles_results.json'
OUTPUT_FILE = './sample_data/codes_dataset.json'
RESUME_FILE = './data/resume_code_2026.json'

def restore_resume_data(current_handle):
    with open(OUTPUT_FILE, 'r+', encoding='utf-8') as op_file:
                resume_check = json.load(op_file)
                for row_data in resume_check:
                    # if row_data["handle"] == current_handle:
                    #     last_object = row_data
                    #     print(last_object)
                    print(row_data)
                    break

# def append_to_json_file(file_path, new_object):
#     with open(file_path, 'r+', encoding='utf-8') as f:
#         # Seek to the end of the file and check the size
#         f.seek(0, 2)  # Move to the end of the file
#         file_size = f.tell()
        
#         # Check if the file is empty or not a valid JSON array
#         if file_size == 0:
#             print("File is empty or not a valid JSON array.")
#             f.write("[]")
#             file_size = f.tell()
        
#         # Move to the second-to-last character
#         f.seek(file_size - 1)  # -2 to skip the last ']'
        
#         # Check if we are in a valid position and the last character is a closing bracket
#         last_char = f.read(1)
#         if last_char == ']':
#             # The array is already complete, so we can safely add a new item
#             # We move back one character to overwrite the last closing bracket
#             f.seek(file_size - 1)
            
#             # Write a comma (if there are items already in the array)
#             if (file_size > 2):
#                 f.write(',')
            
#             # Write the new object (in JSON format)
#             json.dump(new_object, f)
            
#             # Close the JSON array with a closing bracket
#             f.write(']')
#             print(f"Appended new object to {file_path}")
#         else:
#             print(last_char)
#             print("The file does not end with a valid JSON array. Ensure the file is correctly formatted.")
#             return

# # Example usage
# new_data = {"handle": "ksun48",
#         "submission_list": [
#             {
#                 "id": 288561266,
#                 "contestId": 2026,
#                 "creationTimeSeconds": 1730129107,
#                 "relativeTimeSeconds": 3007,
#                 "problem": {
#                     "contestId": 2026,
#                     "index": "F",
#                     "name": "Bermart Ice Cream",
#                     "type": "PROGRAMMING",
#                     "rating": 2700,
#                     "tags": [
#                         "data structures",
#                         "dfs and similar",
#                         "divide and conquer",
#                         "dp",
#                         "implementation",
#                         "trees"
#                     ]
#                 },
#                 "author": {
#                     "contestId": 2026,
#                     "members": [
#                         {
#                             "handle": "ksun48"
#                         }
#                     ],
#                     "participantType": "CONTESTANT",
#                     "ghost": "false",
#                     "startTimeSeconds": 1730126100
#                 },
#                 "programmingLanguage": "C++20 (GCC 13-64)",
#                 "verdict": "OK",
#                 "testset": "TESTS",
#                 "passedTestCount": 197,
#                 "timeConsumedMillis": 1155,
#                 "memoryConsumedBytes": 389939200,
#                 "code": "#include<bits/stdc++.h>\n#pragma GCC optimize(\"Ofast\")\n#pragma GCC optimize(\"unroll-loops\")\n\u00a0\n#define L(i, j, k) for(int i = (j); i <= (k); i++)\n#define R(i, j, k) for(int i = (j); i >= (k); i--)\n#define ll long long\n#define pb emplace_back\n#define ull unsigned long long \n#define sz(a) ((int) a.size())\n#define vi vector<int>\n#define me(a, x) memset(a, x, sizeof(a))\nusing namespace std;\nconst int N = 3007;\nint mod;\nstruct fastmod {\n  typedef unsigned long long u64;\n  typedef __uint128_t u128;\n\u00a0\n  int m;\n  u64 b;\n\u00a0\n  fastmod(int m) : m(m), b(((u128)1 << 64) / m) {}\n  int reduce(u64 a) {\n    u64 q = ((u128)a * b) >> 64;\n    int r = a - q * m;\n    return r < m ? r : r - m;\n  }\n} z(2);\nstruct mint {\n\tint x;\n\tinline mint(int o = 0) { x = o; }\n\tinline mint & operator = (int o) { return x = o, *this; }\n\tinline mint & operator += (mint o) { return (x += o.x) >= mod && (x -= mod), *this; }\n\tinline mint & operator -= (mint o) { return (x -= o.x) < 0 && (x += mod), *this; }\n\tinline mint & operator *= (mint o) { return x = z.reduce((ll) x * o.x), *this; }\n\tinline mint & operator ^= (int b) {\n\t\tmint w = *this;\n\t\tmint ret(1);\n\t\tfor(; b; b >>= 1, w *= w) if(b & 1) ret *= w;\n\t\treturn x = ret.x, *this;\n\t}\n\tinline mint & operator /= (mint o) { return *this *= (o ^= (mod - 2)); }\n\tfriend inline mint operator + (mint a, mint b) { return a += b; }\n\tfriend inline mint operator - (mint a, mint b) { return a -= b; }\n\tfriend inline mint operator * (mint a, mint b) { return a *= b; }\n\tfriend inline mint operator / (mint a, mint b) { return a /= b; }\n\tfriend inline mint operator ^ (mint a, int b) { return a ^= b; }\n};\ninline mint qpow(mint x, int y = mod - 2) { return x ^ y; }\nmint fac[N], ifac[N], inv[N];\nvoid init(int x) {\n\tfac[0] = ifac[0] = inv[1] = 1;\n\tL(i, 2, x) inv[i] = (mod - mod / i) * inv[mod % i];\n\tL(i, 1, x) fac[i] = fac[i - 1] * i, ifac[i] = ifac[i - 1] * inv[i];\n} \nmint C(int x, int y) {\n\treturn x < y || y < 0 ? 0 : fac[x] * ifac[y] * ifac[x - y];\n}\ninline mint sgn(int x) {\n\treturn (x & 1) ? mod - 1 : 1;\n}\n\u00a0\nint n;\nmint g[N][2];\nmint val[N];\nvoid Main() {\n\tcin >> n >> mod;\n\tz = fastmod(mod);\n\tinit(n);\n\tL(i, 0, n) L(o, 0, 1) g[i][o] = 0;\n\tg[0][0] = 1;\n\tL(i, 1, n) \n\t\tg[i][0] = g[i - 1][0] * i + g[i - 1][1], g[i][1] = (g[i - 1][0] + g[i - 1][1]) * i;\n\tL(d, 0, n - 1) {\n\t\tint len = n - d;\n\t\tmint sum = g[d][0] + g[d][1];\n\t\tsum *= fac[n - (len + 1) / 2] * ifac[n - len];\n\t\tsum *= fac[n - len / 2] * ifac[n - len];\n\t\tval[len] = sum;\n\t}\n\tval[0] = qpow(n, n);\n\tL(o, 0, 1) L(i, 1, n) val[i] -= val[i + 1];\n\tL(i, 1, n) val[0] -= val[i];\n\tL(i, 0, n) {\n\t\tcout << val[i].x << ' ';\n\t}\n\tcout << '\\n';\n\tL(i, 0, n) val[i] = 0;\n}\nint main () { \n\tios :: sync_with_stdio(false);\n\tcin.tie (0); cout.tie (0);\n\tint t; cin >> t; while(t--) Main();\n\treturn 0;\n}\n"
#             }
#         ]
#     }
# append_to_json_file("./sample_data/codes_dataset.json", new_data)
# # with open("./sample_data/codes_dataset.json", 'r+', encoding='utf-8') as f:
# #      test_data = json.load(f)
# #      for row in test_data:
# #           print(row)
#         #   break
restore_resume_data("jiangly")