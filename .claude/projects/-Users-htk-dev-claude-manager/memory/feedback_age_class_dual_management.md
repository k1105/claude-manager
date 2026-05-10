---
name: 年齢クラス二重管理の整理課題
description: zuuumyのChild.ageとresolved_age_groupの二重管理を将来的に整理する。ユーザーが覚えておいてと言った課題。
type: project
---

zuuumyの年齢管理にChild.age（DBスナップショット）とresolved_age_group（動的計算）の二重管理がある。

**Why:** ChildQueryは誕生日ベースで動的にフィルタしてるのでChild.ageカラムを使ってない箇所もあり、データの一貫性が保証されてない。

**How to apply:** zuuumyのリファクタや設計議論の際に、この二重管理の解消を提案する候補として覚えておく。詳細は `wiki/concepts/zuuumy-age-class-system.md` を参照。
