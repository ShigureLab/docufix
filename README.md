# Docufix

A simple doc style fixer.

## Installation

```bash
pip install docufix
```

## Usage

Basic usage:

```bash
docufix path-glob1 path-glob2 path-glob3
```

An complex usage:

```bash
docufix path-glob1 path-glob2 path-glob3 \
   --ignore-globs='ignore-glob1,ignore-glob2' \
   --rule1-name \
   --rule1-option1 \
   --rule1-option2 \
   --rule2-name \
   --rule2-option1 \
   --fix
```

### Base options

-  `--fix`，自动修复文件
   -  Type: `bool`
   -  Default: `False`
-  `--ignore-globs`，忽略的文件 glob，多个用 `,` 分隔
   -  Type: str
   -  Default: `""`
-  `--all-rules`，应用所有已有的规则
   -  Type: `bool`
   -  Default: `False`

### Rules

-  中英文间插入空格（对 AST 有改动）
   -  rule name: `--insert-whitespace-between-cn-and-en-char`
-  删除行末空格
   -  rule name: `--trim-trailing-whitespace`
-  统一换行符
   -  rule name: `--unify-newline`
   -  rule options:
      -  `--unify-newline-type`
         -  Type: `Literal["CR", "LF", "CRLF"]`
         -  Default: `LF`
-  确保文件末尾有换行符
   -  rule name: `--ensure-final-newline`
-  删除文件末多余的空行
   -  rule name: `--trim-trailing-blank-lines`
-  使用空格代替 TAB
   -  rule name: `--replace-tab-with-space`
   -  rule options:
      -  `--replace-tab-with-space-indent-size`
         -  Type: `int`
         -  Default: `4`

### Examples

```bash
docufix '**/*.md' '**/*.rst' \
   --ignore-globs='**/README.md,**/index.rst' \
   --insert-whitespace-between-cn-and-en-char \
   --trim-trailing-whitespace \
   --unify-newline \
   --unify-newline-type=LF \
   --ensure-final-newline \
   --trim-trailing-blank-lines \
   --replace-tab-with-space \
   --replace-tab-with-space-indent-size=4 \
   --fix
```
