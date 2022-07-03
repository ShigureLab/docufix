# Docufix

A simple doc style fixer.

## Installation

```bash
pip install docufix
```

## Rules

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

## Usage

```bash
docufix path-glob \
   --rule1-name \
   --rule1-option1 \
   --rule1-option2 \
   --rule2-name \
   --rule2-option1 \
   --fix
```

Example:

```bash
docufix '**/*.md' \
   --insert-whitespace-between-cn-and-en-char \
   --trim-trailing-whitespace \
   --unify-newline \
   --unify-newline-type LF \
   --ensure-final-newline \
   --trim-trailing-blank-lines \
   --fix
```

## Motivation

给 Paddle 的 ReStructuredText 和 Markdown 进行初步的格式化。（下一步是用 Prettier 这样的格式化工具来格式化，因此只是临时解决方案）

## Paddle 文档修缮工程

-  Stage 1: 编写简易脚本工具来全量替换（本阶段）
-  Stage 2: 编写通用工具来格式化文档
-  Stage 3: 完善文档规范，推广文档规范及新的编辑器配置，根据文档规范编写专用工具（linter and autofixer）
-  Stage 4: 设计新的文档维护模式（本阶段也会同时尝试该部分）
