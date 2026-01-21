---
title: Unity逆向中常用的东西 (1)
date: 2025-10-22 08:58:44
tags:
---

## 找 CreateDecompressor

IDA 搜 `Decompressing this format (%d) is not supported on this platform.`

## 找 ArchiveStorageReader::Initialize

IDA 搜 `Unable to read header from archive file: %s`

## LZ4 虚表定义

```c
/*——— 一些占位/前置声明，避免模板与命名空间在 IDA 里不好过编译 ———*/
typedef struct core_string            { void *p; } core_string;           // core::basic_string<char,...> 的占位
typedef struct ShaderLab_SubPrograms  { unsigned char _; } ShaderLab_SubPrograms;
typedef struct ShaderPropertySheet    { unsigned char _; } ShaderPropertySheet;

/* Collider2D::CompositeCapability 是枚举（W4 表示 int 宽度），用 int 代替 */
typedef int Collider2D_CompositeCapability;

/*——— this 指针一律用 void*（x64 下 RCX= this；避免与别的类名冲突） ———*/

/* 0: Lz4Decompressor::`scalar deleting destructor'(uint)  —— ??_GLz4Decompressor@@UEAAPEAXI@Z */
typedef void *(__fastcall *LZ4D_ScalarDeletingDtor_t)(
    void *this_,                      /* Lz4Decompressor* */
    unsigned int flags                /* bit0: delete, bit1: array 等 */
);

/* 1: PolygonCollider2D::GetCompositeCapability(void) —— ?GetCompositeCapability@PolygonCollider2D@@UEBA?AW4CompositeCapability@Collider2D@@XZ */
typedef Collider2D_CompositeCapability (__fastcall *PolygonCollider2D_GetCompositeCapability_t)(
    const void *this_                 /* PolygonCollider2D const* */
);

/* 2: Lz4Decompressor::DecompressMemory(...) —— ?DecompressMemory@Lz4Decompressor@@UEBA_NPEBXPEA_KPEAX1@Z */
typedef bool (__fastcall *Lz4_DecompressMemory_t)(
    const void *this_,                /* Lz4Decompressor const* */
    const void *src,
    unsigned __int64 *pSrcSize,
    void *dst,
    unsigned __int64 *pDstSize
);

/* 3 / 5: SuiteAssetStoreCachePathManagerkUnitTestCategory::GetConfigFixture::GetEnvReturnsFalse(...) [static]
   —— ?GetEnvReturnsFalse@GetConfigFixture@SuiteAssetStoreCachePathManagerkUnitTestCategory@@SA_NAEBV?$basic_string@DV?$StringStorageDefault@D@core@@@core@@AEAV34@@Z
   这是静态函数（SA_），但这里按名义给出原型。 */
typedef bool (__fastcall *SuiteAssetStore_GetEnvReturnsFalse_t)(
    const core_string *name,
    core_string *outValue
);

/* 4: GfxDeviceNull::SetShadersMainThread(ShaderLab::SubPrograms const&, ShaderPropertySheet const*, ShaderPropertySheet const*)
   —— ?SetShadersMainThread@GfxDeviceNull@@UEAAXAEBVSubPrograms@ShaderLab@@PEBVShaderPropertySheet@@1@Z */
typedef void (__fastcall *GfxDeviceNull_SetShadersMainThread_t)(
    void *this_,                                  /* GfxDeviceNull* */
    const ShaderLab_SubPrograms *subPrograms,
    const ShaderPropertySheet   *sheetA,
    const ShaderPropertySheet   *sheetB
);

/*——— 组合成你这段地址上看到的 6 个槽位（0x00..0x28）。注意：接下来出现的
   “??_R4Lz4Compressor@@6B@” 是相邻对象的 RTTI COL，不属于本虚表槽位。 ———*/
struct Lz4Decompressor_vtbl_full
{
    /* 0x00 */ LZ4D_ScalarDeletingDtor_t           dtor_scalar;
    /* 0x08 */ PolygonCollider2D_GetCompositeCapability_t polygon_GetCompositeCapability;
    /* 0x10 */ Lz4_DecompressMemory_t              DecompressMemory;
    /* 0x18 */ SuiteAssetStore_GetEnvReturnsFalse_t GetEnvReturnsFalse_1;   // static，按名义保留签名
    /* 0x20 */ GfxDeviceNull_SetShadersMainThread_t SetShadersMainThread;
    /* 0x28 */ SuiteAssetStore_GetEnvReturnsFalse_t GetEnvReturnsFalse_2;   // 重复出现一次
    /* 之后的 0x30 处不是槽位，而是 Lz4Compressor 的 RTTI 指针，请忽略 */
};

struct Lz4Decompressor
{
    const struct Lz4Decompressor_vtbl_full *vfptr;
    /* ... 其他字段待补 ... */
};
```

## 标准 LoadFromFile 流程

![alt text](LoadFromFile.png)

## 导出汇编 (IDA)

```idc
#include <idc.idc>

static get_idb_dir() {
  auto file_full_path = get_idb_path();
  auto idbdir = qdirname(file_full_path);
  return idbdir;
}

static main() {
  auto cea = ScreenEA();
  msg("ea = 0x08%x\n", cea);

  auto addr_func_start = get_func_attr(cea, FUNCATTR_START);
  auto addr_func_end = get_func_attr(cea, FUNCATTR_END);
  if (addr_func_start != -1 && addr_func_end != -1) {
    if (addr_func_start >= addr_func_end) {
      msg("ERR: start addr <= end addr");
      return;
    }

    msg("func start: %08x\n", addr_func_start);
    msg("func end  : %08x\n", addr_func_end);

    auto filepath = sprintf("%s\\func_%08x.asm", get_idb_dir(), addr_func_start);
    msg("path: %s\n", filepath);
    auto hf = fopen(filepath, "w");
    if (hf != 0) {
      auto f = gen_file(OFILE_LST, hf, addr_func_start, addr_func_end, 0);
      if (f != -1) {
        msg("make asm file ok.\n");
      } else {
        msg("ERR: gen_file error.\n");
      }
    } else {
      msg("ERR: fopen %s error.\n", filepath);
    }
  } else {
    msg("ERR: find func error.\n");
  }
}
```