int __cdecl main(int argc, const char **argv, const char **envp)
{
  size_t v3; // ebx
  int v4; // eax
  int v5; // eax
  int v6; // eax
  int v7; // eax
  int v8; // eax
  int v9; // eax
  int v10; // eax
  int v11; // eax
  int v12; // eax
  int v13; // eax
  int v14; // eax
  int v15; // eax
  int v16; // eax
  int v17; // eax
  int v18; // eax
  int v19; // eax
  int v20; // eax
  int v21; // eax
  int v22; // eax
  int v23; // esi
  int v24; // edi
  int v25; // ebx
  int v26; // ebx
  int v27; // ebx
  int v28; // ebx
  int v29; // ebx
  int v30; // ebx
  int v31; // ebx
  int v32; // ebx
  int v33; // ebx
  int v34; // ebx
  int v35; // eax
  _BYTE v38[332]; // [esp+Ch] [ebp-288h] BYREF
  _DWORD v39[35]; // [esp+158h] [ebp-13Ch]
  char s[30]; // [esp+1E6h] [ebp-AEh] BYREF
  struct stat buf; // [esp+204h] [ebp-90h] BYREF
  int v42; // [esp+25Ch] [ebp-38h]
  int v43; // [esp+260h] [ebp-34h]
  int v44; // [esp+264h] [ebp-30h]
  int v45; // [esp+268h] [ebp-2Ch]
  int v46; // [esp+26Ch] [ebp-28h]
  int v47; // [esp+270h] [ebp-24h]
  int v48; // [esp+274h] [ebp-20h]
  int v49; // [esp+278h] [ebp-1Ch]
  int v50; // [esp+27Ch] [ebp-18h]
  int v51; // [esp+280h] [ebp-14h]
  int *p_argc; // [esp+284h] [ebp-10h]

  p_argc = &argc;
  printf("key:");
  if ( fgets(s, 30, &Stdin) )
  {
    v3 = strcspn(s, "\n"); // 去掉换行符
    s[v3] = 0; // 写 '\0'
    idx_1 = 0;
    // string_to_code("act"); 无意义
    
    // 将 key 的前 10 个字符 转为 数字 存入 v39[25] ~ v39[34]
    // d0=v39[25], d1=v39[26], ..., d9=v39[34]
    for ( strIdx = 0; s[strIdx] && strIdx <= 9; ++strIdx ) // 只处理前 10 个字符
    {
      if ( s[strIdx] <= 48 || s[strIdx] > 57 ) // 非 '1' ~ '9'
      {
        /*
        a ~ f  转 10 ~ 15
        其他字符转 16
        */
        if ( s[strIdx] == 97 ) // a
        {
          v39[idx_1++ + 25] = 10;
        }
        else if ( s[strIdx] == 98 ) // b
        {
          v39[idx_1++ + 25] = 11;
        }
        else if ( s[strIdx] == 99 ) // c
        {
          v39[idx_1++ + 25] = 12;
        }
        else if ( s[strIdx] == 100 ) // d
        {
          v39[idx_1++ + 25] = 13;
        }
        else if ( s[strIdx] == 101 ) // e
        {
          v39[idx_1++ + 25] = 14;
        }
        else if ( s[strIdx] == 102 ) // f
        {
          v39[idx_1++ + 25] = 15;
        }
        else
        {
          if ( s[strIdx] == 48 ) // '0'
            v39[idx_1 + 25] = 0;
          else // 其他字符兜底为 16
            v39[idx_1 + 25] = 16;
          ++idx_1;
        }
      }
      else // '1' ~ '9'
      {
        v39[idx_1++ + 25] = s[strIdx] - 48; // 转数字
      }
    }

    col = 0;
    next = 0;
    v42 = 0;
    v43 = 0;
    v44 = 0;
    v45 = 0;
    v46 = 0;
    v47 = 0;
    for ( row = 0; row <= 4; ++row )
    {
      for ( col = 0; (int)col <= 4; ++col )
      {
        v4 = 0;
        if ( v4 == row && (v5 = 3, v5 == col) ) // (0,3)
        {
          v39[5 * row + col] = v39[next++ + 25]; // d0
          *(_DWORD *)&v38[4 * v42++ + 272] = v39[5 * row + col]; // v42 = 0
        }
        else
        {
          v6 = 1;
          if ( v6 == row && (v7 = 0, v7 == col) ) // (1,0)
          {
            v39[5 * row + col] = v39[next++ + 25]; // d1
            *(_DWORD *)&v38[4 * v43++ + 284] = v39[5 * row + col]; // v43 = 0
          }
          else
          {
            v8 = 1;
            if ( v8 == row && (v9 = 2, v9 == col) ) // (1,2)
            {
              v39[5 * row + col] = v39[next++ + 25]; // d2
              *(_DWORD *)&v38[4 * v42++ + 272] = v39[5 * row + col]; // v42 = 1
              *(_DWORD *)&v38[4 * v44++ + 296] = v39[5 * row + col]; // v44 = 0
            }
            else
            {
              v10 = 2;
              if ( v10 == row && (v11 = 1, v11 == col) ) // (2,1)
              {
                v39[5 * row + col] = v39[next++ + 25]; // d3
                *(_DWORD *)&v38[4 * v42++ + 272] = v39[5 * row + col]; // v42 = 2
                *(_DWORD *)&v38[4 * v43++ + 284] = v39[5 * row + col]; // v43 = 1
              }
              else
              {
                v12 = 2;
                if ( v12 == row && (v13 = 3, v13 == col) ) // (2,3)
                {
                  v39[5 * row + col] = v39[next++ + 25]; // d4
                  *(_DWORD *)&v38[4 * v44++ + 296] = v39[5 * row + col]; // v44 = 1
                  *(_DWORD *)&v38[4 * v45++ + 308] = v39[5 * row + col]; // v45 = 0
                }
                else
                {
                  v14 = 3;
                  if ( v14 == row && (v15 = 0, v15 == col) ) // (3,0)
                  {
                    v39[5 * row + col] = v39[next++ + 25]; // d5
                    *(_DWORD *)&v38[4 * v46++ + 320] = v39[5 * row + col]; // v46 = 0
                  }
                  else if ( row == 3 && col == 2 ) // (3,2) 特例 row==3 && col==2（直接写死） 
                  {
                    v39[5 * row + 2] = v39[next++ + 25]; // d6
                    *(_DWORD *)&v38[4 * v43++ + 284] = v39[5 * row + col]; // v43 = 2
                    *(_DWORD *)&v38[4 * v46++ + 320] = v39[5 * row + col]; // v46 = 1
                  }
                  else
                  {
                    v16 = 3;
                    if ( v16 == row && (v17 = 3, v17 == col) ) // (3,3)
                    {
                      v39[5 * row + col] = v39[next++ + 25]; // d7
                      *(_DWORD *)&v38[4 * v45++ + 308] = v39[5 * row + col]; // v45 = 1
                      *(_DWORD *)&v38[4 * v46++ + 320] = v39[5 * row + col]; // v46 = 2
                    }
                    else
                    {
                      v18 = 3;
                      if ( v18 == row && (v19 = 4, v19 == col) ) // (3,4)
                      {
                        v39[5 * row + col] = v39[next++ + 25]; // d8
                        *(_DWORD *)&v38[4 * v44++ + 296] = v39[5 * row + col]; // v44 = 2
                      }
                      else
                      {
                        v20 = 4;
                        if ( v20 == row && (v21 = 2, v21 == col) ) // (4,2)
                        {
                          v39[5 * row + col] = v39[next++ + 25]; // d9
                          *(_DWORD *)&v38[4 * v45++ + 308] = v39[5 * row + col]; // v45 = 2
                        }
                        else // 其他位置 全部设为 row + col
                        {
                          v39[5 * row + col] = row + col;
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }

        /* 5x5 矩阵 v39
        [ 0, 1, 2, d0, 4 ]
        [ d1, 2, d2, 4, 5 ]
        [ 2, d3, 4, d4, 6 ]
        [ d5, 4, d6, d7, d8 ]
        [ 4, 5, d9, 7, 8 ]
        */

        /* v38 + 272 处存了 15 个数值 (5 行 3 列)
        v42 -> 第一行 d0 d2 d3
        v43 -> 第二行 d1 d3 d6 
        v44 -> 第三行 d2 d4 d8
        v45 -> 第四行 d4 d7 d9
        v46 -> 第五行 d5 d6 d7
        */
        
        v22 = 4;
        if ( v22 == row ) // row==4
          v47 += v39[5 * row + col];
      }
      if ( stat("/etc/rc.d", &buf) ) // 该目录在 QNX 下是存在的 所以不会给 v47 额外加值
        v47 += *(_DWORD *)&v38[12 * row + 272 + 4 * col]; // row = 0 ~ 4, col=0
        
      // v47 最终等于 4 + 5 + 7 + 8 + d9 = 24 + d9
    }

    v48 = 1;
    // 取 v38 + 272 的行和 应该都为 34
    for ( row = 0; row <= 4; ++row ) // row 对应 v42 ~ v46
    {
      v51 = 0;
      for ( col = 0; (int)col <= 2; ++col ) // 每行 3 个数值
      {
        v51 += *(_DWORD *)&v38[12 * row + 272 + 4 * col];
        v51 -= 5;
      }
      if ( v51 != 19 ) // 每一行的和-15 应该都为 19 -> 每一行的和应该都为 34
        v48 = 0;
    }

    /*
    可得等式
    d0 + d2 + d3 = 34
    d1 + d3 + d6 = 34
    d2 + d4 + d8 = 34
    d4 + d7 + d9 = 34
    d5 + d6 + d7 = 34
    */

    memset(v38, 0, 0x110u);                 // 在 QNX 这两步成功 所以不会给 v47 额外 +1
    v49 = open("/proc/self/as", (int)"r");      
    if ( v49 == -1 )
      ++v47;
    if ( devctl(v49, 1091569665, v38, 272, 0) )
      ++v47;

    v23 = v47;
    v24 = v39[0] + v39[3] * v39[2] * v39[1] * v39[4] + (v38[8] & 0x80); // 0 + d0 * 2 * 1 * 4 = 8 * d0 | (v38[8]&0x80) 在 QNX 是 0
    v25 = 4 + 1; // 5
    // if ( v23 != v24 + v25 * ~4 - 9 ) 
    // if ( v47 != v24 + 5 * ~4 - 9 )  // 5 * ~4 - 9 = 5*(-5) - 9 = -34
    if ( v47 != v24 - 34 )  // 5 * ~4 - 9 = 5*(-5) - 9 = -34
      v48 = 0;              // v47 应为 8*d0 - 34
                            // 前文已知 v47 = 24 + d9
                            // 24 + d9 = 8*d0 - 34 -> 8*d0 - d9 = 58 | 又因为 d0,d9 范围均为 0 ~ 15 | (d0,d9)∈{(8,6), (9,14)}

    // 末 4 位 'a'/'s' 
    v50 = 123;
    v26 = 2 * 4;
    if ( s[v26 + 2] == 97 ) // s[10]: 'a' +45 / 's' -45
      v50 += 45;
    v27 = 2 * 4;
    if ( s[v27 + 2] == 115 )
      v50 -= 45;
    v28 = 2 * 4;
    if ( s[v28 + 3] == 97 ) // s[11]: 'a' +67 / 's' -67
      v50 += 67;
    v29 = 2 * 4;
    if ( s[v29 + 3] == 115 )
      v50 -= 67;
    v30 = 2 * 4;
    if ( s[v30 + 4] == 97 ) // s[12]: 'a'  +8 / 's'  -8
      v50 += 8;
    v31 = 2 * 4;
    if ( s[v31 + 4] == 115 )
      v50 -= 8;
    v32 = 3 * 4;
    if ( s[v32 + 1] == 97 ) // s[13]: 'a'  +9 / 's'  -9
      v50 += 9;
    v33 = 3 * 4;
    if ( s[v33 + 1] == 115 )
      v50 -= 9;
    v34 = 4;
    v35 = 1;
    if ( 20 * (v34 + v35) != v50 ) // 100 != v50 -> v50 应为 100
                                   // 100 = 123 + 45 - 67 + 8 -9 即 s[10]='a', s[11]='s', s[12]='a', s[13]='s'
      v48 = 0;
    if ( v48 == 1 && strlen(s) <= 0xE ) // key 长度 <= 14 -> key 最多 10 个有效字符 + "asas"
      puts("ok");
    else
      puts("no");
    return 0;
  }
  else
  {
    puts("error");
    return 1;
  }
}