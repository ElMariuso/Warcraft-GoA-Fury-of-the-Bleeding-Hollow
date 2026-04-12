# Data Types — CK3 GUI & Localization Reference

> **Vue rapide** : Types de données CK3 utilisés dans le GUI et la localisation. Accès via `[GetPlayer.GetName]` dans les fichiers `.gui` et `.yml`. Source : console `DumpDataTypes` → `data_types.log`.

---

## Fonctionnement

Chaînés avec `.` dans `[ ]` : `[GetPlayer.GetSpouse.GetName]`. Un **Promote** retourne un type, une **Function** opère dessus.

---

## Global Promotes (les plus utiles)

| Promote               | Type retourné  | Description                        |
| --------------------- | -------------- | ---------------------------------- |
| `GetPlayer`           | Character      | Le joueur actuel                   |
| `CHARACTER`           | Character      | Personnage en contexte             |
| `TITLE`               | Title          | Titre en contexte                  |
| `SCOPE`               | TopScope       | Scope racine                       |
| `ROOT`                | Scope          | Scope root du script               |
| `PREV`                | Scope          | Scope précédent                    |
| `GetCurrentDate`      | Date           | Date actuelle du jeu               |
| `GetTitleByKey`       | Title          | Titre par clé (ex: `k_england`)    |
| `GetFaithByKey`       | Faith          | Foi par clé                        |
| `GetTrait`            | Trait          | Trait par ID                       |
| `GetModifier`         | StaticModifier | Modificateur par clé               |
| `GetGlobalVariable`   | Scope          | Variable globale                   |
| `GetNullCharacter`    | Character      | Character null (pour comparaisons) |
| `GetDynastyByID`      | Dynasty        | Dynastie par ID numérique          |
| `GetDynastyHouseByID` | DynastyHouse   | Maison par ID                      |
| `GetDecision`         | Decision       | Décision par clé                   |
| `GetSchemeType`       | SchemeType     | Type de scheme                     |

## Global Functions (les plus utiles)

| Function                  | Type retourné | Description              |
| ------------------------- | ------------- | ------------------------ |
| `Localize`                | CString       | Localise une clé         |
| `Concatenate`             | CString       | Concatène des strings    |
| `Not`                     | bool          | Négation booléenne       |
| `And` / `Or`              | bool          | Opérateurs logiques      |
| `Add_int32`               | int32         | Addition entière         |
| `Subtract_int32`          | int32         | Soustraction             |
| `Multiply_int32`          | int32         | Multiplication           |
| `Max_int32` / `Min_int32` | int32         | Min/max                  |
| `Select_int32`            | int32         | Sélection conditionnelle |
| `EqualTo_int32`           | bool          | Comparaison d'égalité    |
| `GreaterThan_int32`       | bool          | Comparaison >            |
| `IntToFloat`              | float         | Conversion int → float   |

Les variantes `_CFixedPoint`, `_float`, `_uint32` existent pour chaque opérateur.

---

## Types principaux

### Character

| Function           | Retour      | Description       |
| ------------------ | ----------- | ----------------- |
| `GetName`          | CString     | Nom du personnage |
| `GetAge`           | int32       | Age               |
| `GetGold`          | CFixedPoint | Or                |
| `GetPrestige`      | CFixedPoint | Prestige          |
| `GetPiety`         | CFixedPoint | Piété             |
| `GetFaith`         | Faith       | Foi du personnage |
| `GetCulture`       | Culture     | Culture           |
| `GetDynasty`       | Dynasty     | Dynastie          |
| `GetSpouse`        | Character   | Conjoint          |
| `GetLiege`         | Character   | Suzerain          |
| `GetPrimaryTitle`  | Title       | Titre principal   |
| `GetCapitalCounty` | County      | Comté capital     |

### Title

| Function         | Retour    | Description                |
| ---------------- | --------- | -------------------------- |
| `GetName`        | CString   | Nom du titre               |
| `GetHolder`      | Character | Détenteur actuel           |
| `GetDeJureLiege` | Title     | Liège de jure              |
| `GetTier`        | int32     | Rang (1=barony → 5=empire) |

### County

| Function     | Retour  | Description      |
| ------------ | ------- | ---------------- |
| `GetName`    | CString | Nom du comté     |
| `GetCulture` | Culture | Culture du comté |
| `GetFaith`   | Faith   | Foi du comté     |

### Dynasty / DynastyHouse

| Function         | Retour      | Description         |
| ---------------- | ----------- | ------------------- |
| `GetName`        | CString     | Nom                 |
| `GetPrestige`    | CFixedPoint | Prestige dynastique |
| `GetHeadOfHouse` | Character   | Chef de maison      |
| `GetDynastyHead` | Character   | Chef de dynastie    |

### Faith / Religion

| Function         | Retour   | Description           |
| ---------------- | -------- | --------------------- |
| `GetName`        | CString  | Nom de la foi         |
| `GetReligion`    | Religion | Religion parente      |
| `GetHighGodName` | CString  | Nom du dieu principal |

### Culture / War / Scope

| Type    | Function          | Retour       | Description         |
| ------- | ----------------- | ------------ | ------------------- |
| Culture | `GetName`         | CString      | Nom de la culture   |
| Culture | `GetCultureGroup` | CultureGroup | Groupe culturel     |
| War     | `GetAttacker`     | Character    | Attaquant principal |
| War     | `GetDefender`     | Character    | Défenseur principal |
| Scope   | `Var`             | Scope        | Accès aux variables |
