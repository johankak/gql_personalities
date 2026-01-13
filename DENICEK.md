# Úkol
## Dosažená vzdělání, zaměstnání, vyznamenání, hodnosti (gql_personalities)
- Rank
- Study place
- WorkHistoryPosition 
- MedalType 
- CertificateType

# Časová posloupnost hlavních commitů
## 18. 10. 2025
- Záčátek práce na našem projektu.
- Jako první jsme zvolili zprovoznit tabulku typů hodností na hodině za pomoci prof. Štefka a další typy zpracovat na základě RankModel.

## 4. 11. 2025
- Zprovoznění UserRankModel a UserRankGQLModel
- Tyto modely přiřazují uživatele k hodnosti
- Zprovoznili jsme je opět na hodině za pomoci prof. Štefka, další přiřazující modely také vycházejí z těchto základní modelů hodností.

## 8. 11. 2025
- Vytvořili jsme problém, který spočíval v tom, že jsme špatně pojmenovali modely Ranks, UserRanks.
- Tato chyba se propsala do několika souborů
- V tomto commitu jsme už kompletně přejmenovali všechny potřebné symboly a tento problém vyřešili

## 8.-9. 11. 2025
- Vytvoření čtyř typů: StudyPlace, WorkHistoryPosition, MedalType, MedalCategory na základě Rank
- Původně jsme vytvořili MedalType a MedalCategory, ale později jsme je sloučili do MedalType a implementovali stromovou strukturu

## 24. 11. 2025
- Dokončení zprovoznění mutací Insert, Update a Delete u dosavadních typů
- Zatím bez extensions na přihlašování, ty jsme zprovoznili později

## 15. 12. 2025
- Zprovoznění mutací u UserRankGQLModel
- Fungují i extensions na přihlašování, přidali jsme do systemdata rbacobject id
- U dalších typů jsme zprovoznili tyto extensions na základě UserRankGQLModel

## 21. 12. 2025
- Zprovoznění UserAbsoluteAccessControlExtension u základní "typů typů"
- Předtím jsme tam měli posloupnost extensions s rbac objectem, ale to nebylo potřeba

## 5. 1. 2026
- Zprovoznění stromové struktury u CertificateType
- Odstranili jsme CertificateCategory
- Přidali jsme parent_id ke každému certifikátu
- Stromovou strukturu u ostatních typů jsme zprovoznili na základě tohoto

## 12. 1. 2026
- Odstranění zbytků SimpleDeletePermission u všech souborů
- Odstranění zbytků základu na stromovou strukturu u vázaných typů

