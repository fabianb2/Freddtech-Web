# FREDDTECH WEB — primera versión funcional

**Pequeñas apps. Grandes soluciones.**

Sitio corporativo estático para FREDDTECH, listo para revisión local y posterior despliegue gratuito en Cloudflare Pages. Proyecto existente: repositorio `fabianb2/Freddtech-Web` y sitio https://freddtech-web.pages.dev/. Los cambios locales requieren revisión antes de subirlos, pues la integración Git puede publicarlos automáticamente.

## Incluido

- Inicio con diseño responsive y representación visual conceptual (NO son capturas reales de Android).
- Catálogo y fichas individuales: **¿Dónde Quedó?** (disponible en Google Play) y **¿Cuánto Queda?** (en planificación).
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
- **Logotipo FREDDTECH:** actualizado según la ilustración proporcionada por el usuario: cuadro azul con esquinas redondeadas y F curva en blanco y azul claro. Reemplaza el símbolo geométrico anterior. Versiones vectoriales en `public/assets/img/freddtech-symbol.svg`, `freddtech-logo.svg` (fondo transparente) y `freddtech-logo-dark.svg` (fondo oscuro). Símbolo utilizado en cabecera, pie y favicon. Los iconos y capturas oficiales de las aplicaciones siguen pendientes.
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

El icono oficial de ¿Dónde Quedó? se conserva en `public/assets/img/donde-quedo-icon.png`, obtenido de los recursos del proyecto Android. Estado de producción confirmado por el propietario el 4 de noviembre de 2026.

## Verificación de AdSense

Cuenta de editor `ca-pub-1728686227442320`, proporcionada por el propietario. La metaetiqueta `google-adsense-account` se genera dentro de `<head>`. En AdSense seleccionar **Metaetiqueta** para verificar y después solicitar revisión. Esta actualización solo verifica la propiedad; no carga scripts publicitarios ni muestra anuncios.

## Preparación publicitaria — 5 de noviembre de 2026

- Política de privacidad de la web: `public/privacidad/web/index.html`, separada de las apps y enlazada en todos los pies de página.
- Estrategia elegida: un bloque display adaptable en Inicio después de la sección de aplicaciones. Sin anuncios en Soporte, Privacidad, Términos ni 404; sin superposiciones, intersticiales ni ventanas emergentes. La ubicación se marca como comentario HTML, sin reservar espacio vacío.
- Aún no se cargan scripts publicitarios. La activación se implementará con el identificador real del bloque y la CMP publicada; no se inventan identificadores ni se simula el consentimiento.
- Pendiente en la cuenta: Sitios debe indicar Listo; crear y publicar el mensaje de consentimiento en Privacidad y mensajería (consentir, no consentir y gestionar opciones), con enlace a https://freddtech-web.pages.dev/privacidad/web/ y posibilidad de revocar; crear un bloque Display adaptable y obtener su código/identificador. Mantener anuncios automáticos apagados para controlar la ubicación.
- Con ese código: incorporar la carga de AdSense y una única solicitud del bloque, actualizar la política para describir los anuncios activos y adaptar CSP a las solicitudes verificadas del anuncio y la CMP. Mantener `base-uri`, `object-src`, `frame-ancestors` y restricciones de permisos; no eliminar toda la CSP ni introducir permisos globales sin verificar.
- Probar consentimiento/rechazo/revocación, ausencia de solicitudes duplicadas, anuncios sin rellenar, bloqueo de publicidad, móvil y escritorio. Confirmar que el contenido se mantiene legible y los enlaces de soporte siguen funcionando. Después activar y verificar en producción.

## Integración AdSense instalada — 5 de noviembre de 2026

Esta sección actualiza la preparación anterior. Bloque Display adaptable `1959689089`, editor `ca-pub-1728686227442320`, proporcionados por el propietario. El propietario confirmó mediante captura el mensaje europeo Publicado.

- Un único bloque en Inicio, después de las aplicaciones. No se inserta en otras páginas ni en 404. Mantener anuncios automáticos apagados en la cuenta para conservar el control manual; esa opción no se puede confirmar desde el código.
- `assets/js/ads.js` carga el código oficial una sola vez, prepara `googlefc.callbackQueue`, solicita el bloque y permite revocar mediante la API cuando está disponible. No simula una CMP ni añade su propio consentimiento. La entrega y decisión de consentimiento las gestiona Google.
- Oculta el bloque ante error de carga o estado `unfilled`. Reserva altura mientras se solicita para limitar cambios de diseño. No reintenta ni refresca anuncios.
- `_headers` conserva `base-uri`, `object-src`, `frame-ancestors`, HTTPS y los otros encabezados. Las páginas sin anuncios aplican una CSP restrictiva mediante metaetiqueta. Inicio usa una política de scripts con hash SHA-256 y `strict-dynamic` para el pequeño cargador de confianza; permite los estilos y recursos de anuncios de terceros y `unsafe-eval`, requerido por el soporte CSP de AdSense. No se usa un nonce fijo ni listas de dominios que Google advierte que pueden quedar obsoletas.
- `check_site.py` verifica los hashes de scripts inline y solo admite el cargador en Inicio. Cambiar el cargador requiere regenerar la política. La página 404 se genera con CSP normal y sin cargador publicitario.
- La política de privacidad de la web describe la integración instalada. El sitio puede seguir sin mostrar anuncios mientras Google revisa su aprobación. No se ha confirmado la opción de anuncios automáticos ni la entrega de un anuncio real desde la cuenta.

Fuentes técnicas: https://support.google.com/adsense/answer/16283098 y https://developers.google.com/funding-choices/fc-api-docs .
