# FREDDTECH WEB — primera versión funcional

**Pequeñas apps. Grandes soluciones.**

Sitio corporativo estático para FREDDTECH, listo para revisión local y posterior despliegue gratuito en Cloudflare Pages. Proyecto existente: repositorio `fabianb2/Freddtech-Web` y sitio https://freddtech-web.pages.dev/. Los cambios locales requieren revisión antes de subirlos, pues la integración Git puede publicarlos automáticamente.

## Incluido

- Inicio con diseño responsive y representación visual conceptual (NO son capturas reales de Android).
- Catálogo y fichas individuales: **¿Dónde Quedó?** (prueba cerrada en Google Play) y **¿Cuánto Queda?** (en planificación).
- Sobre FREDDTECH, soporte con FAQ, novedades.
- Apartados separados para privacidad por app y términos de uso, claramente indicados como **pendientes**, sin inventar documentos legales.
- Navegación de móvil accesible; enlaces internos relativos para que la web se pueda revisar localmente.
- HTML semántico, CSS y JavaScript sin librerías externas, sin cookies analíticas, sin formularios falsos ni fuentes de terceros.
- Encabezados de seguridad de Cloudflare Pages en `public/_headers`.

## Estructura

```text
freddtech-web/
├── public/                    <- DIRECTORIO PUBLICABLE en Cloudflare
│   ├── index.html
│   ├── 404.html
│   ├── _headers
│   ├── robots.txt
│   ├── assets/
│   │   ├── css/styles.css
│   │   ├── js/site.js
│   │   └── img/icons.svg
│   ├── aplicaciones/
│   │   ├── index.html
│   │   ├── donde-quedo/index.html
│   │   └── cuanto-queda/index.html
│   ├── nosotros/index.html
│   ├── soporte/index.html
│   ├── privacidad/
│   │   ├── index.html
│   │   ├── donde-quedo/index.html
│   │   └── cuanto-queda/index.html
│   ├── novedades/index.html
│   └── terminos/index.html
├── tools/
│   ├── generate.py           <- Genera las páginas HTML; biblioteca estándar
│   └── check_site.py         <- Comprueba enlaces internos y estructura
├── README.md
└── .gitignore
```

## Revisar la web sin publicarla

Opción sencilla: extrae el ZIP y abre `public/index.html` en un navegador. Debido a las políticas locales de algunos navegadores, ciertos iconos SVG pueden no mostrarse al abrir directamente `file://`.

Para verla como web real, desde un equipo con Python instalado:

```bash
cd freddtech-web
python3 -m http.server 8000 --directory public
```

Abre `http://localhost:8000/`.

## Configuración de Cloudflare Pages (SOLO cuando apruebes publicar)

1. Desde Chrome en tu Android entra en [github.com/new](https://github.com/new).
2. Crea un repositorio llamado `freddtech-web`; activa README si lo deseas, pero reemplázalo con el de este ZIP al subir los archivos. No reutilices el proyecto Android.
3. Sube **los contenidos del ZIP conservando la estructura**. Es importante que `public/index.html` quede dentro del directorio `public` en la raíz del repositorio.
4. Inicia sesión en [dash.cloudflare.com](https://dash.cloudflare.com/). Abre **Workers & Pages** y crea un nuevo **proyecto Pages** con integración de Git (la interfaz puede variar).
5. Autoriza únicamente el repositorio `freddtech-web`, si Cloudflare ofrece esta opción.
6. Configura:

| Campo | Valor |
|---|---|
| Framework preset | None |
| Production branch | `main` (o la rama principal real) |
| Root directory | raíz del repositorio |
| Build command | `exit 0` |
| Build output directory | `public` |
| Project name | `freddtech` *si está disponible* |

7. **Antes de pulsar Deploy**, comprueba visuales, soporte y políticas. `freddtech.pages.dev` solo existirá si Cloudflare acepta ese nombre; de lo contrario se asignará otro.
8. Cuando autorices el primer despliegue, Cloudflare emitirá HTTPS en el subdominio `pages.dev`. Con integración Git, **las confirmaciones futuras en `main` podrán publicarse automáticamente**. Revisa antes de aprobar o fusionar cambios.

Documentación oficial: [Cloudflare Pages — Git](https://developers.cloudflare.com/pages/configuration/git-integration/github-integration/) y [Static HTML](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/).

### Desde Android: carga de archivos

GitHub permite `Add file > Upload files`, pero cargar toda la estructura desde el móvil puede ser incómodo. **No subas el ZIP como único archivo dentro del repositorio**: Cloudflare no lo descomprime automáticamente. Pide a Codex que cree los archivos directamente en `freddtech-web` o usa una herramienta Git capaz de cargar carpetas manteniendo rutas. En Chrome puedes activar *Sitio para computadoras*.

## Cómo mantener el sitio

- **Textos, fichas y secciones:** edita `tools/generate.py`, luego ejecuta `python3 tools/generate.py` y confirma también los archivos HTML de `public/`. Alternativamente, Codex puede modificar directamente el HTML de `public/`, pero en ese caso también debe sincronizar el generador.
- **Colores:** `public/assets/css/styles.css`, variables `:root`.
- **Menú e interacciones:** `public/assets/js/site.js`.
- **Más aplicaciones:** crea entrada y ficha en el generador, luego regenera.
- **Logotipo FREDDTECH:** identidad Premium Geometric incorporada: F geométrica en azul oscuro y azul corporativo, con el eslogan «Pequeñas apps. Grandes soluciones.». Archivos vectoriales transparentes en `public/assets/img/freddtech-symbol.svg` y `freddtech-logo.svg`; símbolo utilizado en cabecera, pie y favicon. Los iconos y capturas oficiales de las aplicaciones siguen pendientes.
- **Contacto:** correo oficial confirmado: `freddtech26@gmail.com`, presente en Soporte, fichas de aplicaciones y pie de página mediante `mailto:`. El visitante debe enviar el mensaje desde su aplicación o servicio de correo; el sitio no envía mensajes ni simula confirmaciones de envío.
- **Privacidad:** hay que verificar y enlazar la URL oficial actual de la política de «¿Dónde Quedó?». **No reemplaces una URL registrada en Play Console** sin garantizar continuidad. «¿Cuánto Queda?» necesitará su propia política al definir el tratamiento de datos.
- **Novedades:** añadir noticias reales con fechas verificadas, no hitos ficticios.
- **Sitemap/canonical:** añadir después de obtener un dominio o subdominio real y definitivo. No se inventan URLs.

## Seguridad

El archivo `public/_headers` configura CSP restrictiva, `X-Frame-Options`, `X-Content-Type-Options`, política de referencias y restricciones de permisos. Cloudflare Pages aplica estos encabezados a activos estáticos; **no los aplica a Pages Functions** si se agregan en el futuro. Las rutas actuales no utilizan Functions.

Esta web **no realiza transmisiones de datos personales** por sí misma ni almacena cuentas o claves; para integraciones futuras hay que hacer una revisión de seguridad y privacidad nueva.

## Comprobaciones y límites

```bash
python3 tools/check_site.py
```

Las revisiones estáticas comprueban existencia de enlaces y archivos, encabezados básicos, títulos, estructura y ausencia de código inline. Se comprobó una vista de escritorio de 1440px y una móvil de 390px con Chromium mediante una representación local en memoria. **Aún falta validar en el dominio real con HTTPS, Lighthouse, navegadores móviles físicos y revisar los enlaces legales finales.**

## Condiciones de uso del código

Código inicial de trabajo para FREDDTECH. Esta entrega no modifica ni publica aplicaciones Android, no conecta repositorios ajenos y no instala servicios.
