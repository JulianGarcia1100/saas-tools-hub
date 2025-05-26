@echo off
echo ========================================
echo   Building SEO Affiliate Site
echo ========================================

cd ..\hugo_site

echo Building site with Hugo...
C:\Users\garci\hugo\bin\hugo.exe --minify

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Site built successfully!
    echo.
    echo 📁 Generated files in: hugo_site\public\
    echo 🌐 Ready for deployment to Netlify
    echo.
    echo 🚀 Next steps:
    echo    1. Deploy to Netlify: Drag hugo_site\public\ folder to Netlify
    echo    2. Or use Git deployment for automation
    echo    3. Configure custom domain if desired
    echo.
) else (
    echo ❌ Build failed!
    pause
    exit /b 1
)

pause
