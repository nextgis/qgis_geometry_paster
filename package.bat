mkdir geometry_paster
mkdir geometry_paster\i18n
xcopy src\geometry_paster\*.py geometry_paster
xcopy src\geometry_paster\*.ui geometry_paster
xcopy src\geometry_paster\*.svg geometry_paster
xcopy README.md geometry_paster
xcopy LICENSE geometry_paster
xcopy metadata.txt geometry_paster
xcopy i18n\*.ts geometry_paster\i18n\
lrelease geometry_paster\i18n\geometry_paster_ru.ts
lrelease geometry_paster\i18n\geometry_paster_fr.ts
lrelease geometry_paster\i18n\geometry_paster_de.ts
lrelease geometry_paster\i18n\geometry_paster.ts
zip -r geometry_paster.zip geometry_paster
del /s /q geometry_paster
rmdir /s /q geometry_paster