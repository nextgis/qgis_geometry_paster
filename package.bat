mkdir geometry_paster
mkdir geometry_paster\i18n
xcopy *.py geometry_paster
xcopy README.md geometry_paster
xcopy LICENSE geometry_paster
xcopy metadata.txt geometry_paster
xcopy icon.svg geometry_paster
xcopy /F i18n\*.qm geometry_paster\i18n
zip -r geometry_paster.zip geometry_paster
rmdir /S /Q geometry_paster