#!/usr/bin/env python3
"""Regenera páginas estáticas FREDDTECH con solo la biblioteca estándar de Python.
Salida en public/. No publica ni interactúa con cuentas externas.
"""
from pathlib import Path
from html import escape
import hashlib
import base64
ROOT = Path(__file__).resolve().parent.parent / "public"
PLAY_URL = "https://play.google.com/store/apps/details?id=com.freddtech.dondequedo"

def play_button():
    return f'<a href="{PLAY_URL}" class="btn btn-primary">Descargar en Google Play</a>'




def ic(name: str) -> str:
    return f'<svg class="icon" aria-hidden="true"><use href="{{{{ASSET}}}}assets/img/icons.svg#{escape(name)}"></use></svg>'


def link(label: str, path: str, klass: str = "", icon: str = "") -> str:
    return f'<a href="{{{{ROOT}}}}{path}" class="{klass}">{escape(label)} {ic(icon) if icon else ""}</a>'


def badge(text: str, kind: str = "blue") -> str:
    return f'<span class="badge badge-{kind}"><span class="bullet"></span>{escape(text)}</span>'


def breadcrumb(segments):
    parts = [link("Inicio", "")]
    for title, url in segments[:-1]:
        parts.append(ic("chevron"))
        parts.append(link(title, url))
    parts.append(ic("chevron"))
    parts.append(f'<span aria-current="page">{escape(segments[-1][0])}</span>')
    return '<nav aria-label="Ruta de navegación" class="breadcrumb">' + "".join(parts) + '</nav>'


def section_hero(label, heading, intro, bc=None):
    crumbs = breadcrumb(bc) if bc else ""
    return f'''<section class="page-hero"><div class="container">{crumbs}
    <span class="eyebrow"><span class="dot"></span>{label}</span>
    <h1>{heading}</h1><p>{intro}</p></div></section>'''


def app_visual(which, style="app-visual", caption=True):
    if which == 'box':
        cls = 'detail-art' if style == 'detail-art' else 'app-visual mint'
        cap = '<span class="visual-caption">Icono oficial</span>' if caption and style != 'detail-art' else ''
        return f'<div class="{cls}" aria-label="Icono oficial de ¿Dónde Quedó?"><div class="app-symbol official-app-symbol"><img src="{{{{ASSET}}}}assets/img/donde-quedo-icon.png" width="512" height="512" alt="Icono de ¿Dónde Quedó?: una caja sonriente sobre fondo azul"></div>{cap}</div>'
    mint = which == 'box'
    icon = 'box' if mint else 'calendar'
    cls = 'mint' if mint else 'peach'
    if style == 'detail-art':
        return f'<div class="detail-art {"" if mint else "peach"}" aria-label="Ilustración conceptual, no es un icono ni captura oficial"><div class="app-symbol">{ic(icon)}</div></div>'
    cap = '<span class="visual-caption">Ilustración conceptual</span>' if caption else ''
    return f'<div class="app-visual {cls}" aria-label="Ilustración conceptual, no es un icono oficial"><div class="app-symbol">{ic(icon)}</div>{cap}</div>'


def app_card(which):
    if which == 'box':
        name, status, kind, quote, desc, url = '¿Dónde Quedó?', 'En producción en Google Play', 'blue', 'Menos buscar, más vivir.', 'Recuerda dónde guardaste tus objetos y encuentra cada cosa cuando la necesites.', 'aplicaciones/donde-quedo/'
    else:
        name, status, kind, quote, desc, url = '¿Cuánto Queda?', 'En planificación', 'peach', 'Menos desperdicio, más ahorro.', 'Organiza productos, revisa fechas de caducidad y recibe alertas antes de su vencimiento.', 'aplicaciones/cuanto-queda/'
    return f'''<article class="app-card">{app_visual(which)}<div class="card-content">{badge(status,kind)}<h3>{name}</h3><p>{desc}</p>
      <div class="card-bottom"><strong>{quote}</strong>{link('Ver detalles',url,'','arrow-right')}</div>{play_button() if which == 'box' else ''}</div></article>'''


def foot_note():
    return '<p class="small muted">FREDDTECH no solicita datos personales desde esta web en su versión inicial. No se utilizan formularios ni herramientas de seguimiento.</p>'


def home():
    return f'''<section class="hero"><div class="container hero-grid"><div class="hero-copy">
      <span class="eyebrow"><span class="dot"></span> Tecnología útil, todos los días</span>
      <h1>Pequeñas apps.<br><span class="text-blue">Grandes soluciones.</span></h1>
      <p class="hero-description">Desarrollamos herramientas sencillas e intuitivas para resolver problemas reales de la vida cotidiana. Menos complicaciones, más tiempo para ti.</p>
      <div class="buttons">{link('Explorar aplicaciones','aplicaciones/','btn btn-primary','arrow-right')}{link('Conoce FREDDTECH','nosotros/','btn btn-secondary')}</div>
      <div class="hero-meta"><span>{ic('check')} Diseño intuitivo</span><span>{ic('check')} Soluciones prácticas</span><span>{ic('check')} Tecnología accesible</span></div>
    </div><div class="hero-art" aria-label="Ilustración conceptual de la experiencia de una app de organización">
      <div class="art-halo"></div><div class="phone-shell" aria-hidden="true"><div class="phone-top"></div><div class="phone-screen">
      <div class="phone-text-sm">ORGANIZA TU DÍA</div><div class="phone-title">Todo en su lugar.</div>
      <div class="screen-search">{ic('search')} Encuentra lo que necesitas</div>
      <p class="screen-list-title">Tus espacios</p>
      <div class="screen-item"><span class="screen-symbol">{ic('box')}</span><span class="screen-lines"><span class="screen-line"></span><span class="screen-line short"></span></span></div>
      <div class="screen-item"><span class="screen-symbol peach">{ic('layers')}</span><span class="screen-lines"><span class="screen-line"></span><span class="screen-line short"></span></span></div>
      <div class="screen-item"><span class="screen-symbol">{ic('check')}</span><span class="screen-lines"><span class="screen-line"></span><span class="screen-line short"></span></span></div>
      </div><div class="phone-footer"><span></span><span></span><span></span></div></div>
      <div class="float-note note-one" aria-hidden="true"><span class="note-symbol">{ic('spark')}</span><span><strong>Menos estrés</strong><small>Todo más sencillo</small></span></div>
      <div class="float-note note-two" aria-hidden="true"><span class="note-symbol">{ic('check')}</span><span><strong>Más tranquilidad</strong><small>Pequeñas soluciones</small></span></div>
      <div class="art-disclaimer">Representación visual conceptual · No es una captura real</div>
    </div></div></section>
    <div class="trust-strip"><div class="container trust-grid"><span class="trust-lead">Así entendemos la tecnología</span>
       <span class="trust-item">{ic('bolt')} Simple de usar</span><span class="trust-item">{ic('heart')} Pensada para personas</span><span class="trust-item">{ic('shield')} Privacidad consciente</span>
    </div></div>
    <section class="section" id="aplicaciones"><div class="container"><div class="section-head"><span class="eyebrow">01 / Nuestras aplicaciones</span>
      <h2>Apps que hacen tu día <span class="text-blue">más fácil.</span></h2><p>Cada proyecto empieza con una necesidad cotidiana y una pregunta: ¿cómo podemos resolverla de forma más simple?</p></div>
      <div class="app-grid">{app_card('box')}{app_card('calendar')}</div>
      <div class="space-top-27">{link('Conocer todas las aplicaciones','aplicaciones/','btn btn-plain','arrow-right')}</div>
    </div></section>
    <aside class="ad-section" aria-label="Publicidad"><div class="container"><p class="ad-label">Publicidad</p><ins class="adsbygoogle" data-ad-client="ca-pub-1728686227442320" data-ad-slot="1959689089" data-ad-format="auto" data-full-width-responsive="true"></ins></div></aside>
    <section class="section band"><div class="container band-grid"><div><span class="eyebrow eyebrow-light">02 / Nuestro enfoque</span>
      <h2>La tecnología debería ayudarte, no complicarte.</h2>
      <p>En FREDDTECH creemos que la mejor aplicación no es la que más funciones tiene, sino la que resuelve bien lo que necesitas.</p>
      {link('Nuestra filosofía','nosotros/','btn btn-secondary','arrow-right')}</div>
      <div class="value-list">
        <div class="value-row"><span class="value-icon">{ic('search')}</span><div><h3>Problemas reales</h3><p>Partimos de situaciones que ocurren todos los días.</p></div></div>
        <div class="value-row"><span class="value-icon">{ic('bolt')}</span><div><h3>Experiencias simples</h3><p>Interacciones directas, claras y sin pasos innecesarios.</p></div></div>
        <div class="value-row"><span class="value-icon">{ic('shield')}</span><div><h3>Confianza y cuidado</h3><p>Buenas prácticas de privacidad, calidad y seguridad.</p></div></div>
      </div></div></section>
    <section class="section"><div class="container"><div class="section-head"><span class="eyebrow">03 / Mantente al día</span><h2>Lo nuevo en <span class="text-blue">FREDDTECH.</span></h2>
       <p>Conoce nuestras aplicaciones en preparación y los siguientes pasos del proyecto.</p></div>
       <div class="news-list"><article class="news-card"><span class="kicker">En preparación</span><h3>Un espacio para nuestras aplicaciones</h3><p>Estamos construyendo un sitio donde explorar cada solución y encontrar su información oficial.</p></article>
       <article class="news-card"><span class="kicker">Próximamente</span><h3>¿Cuánto Queda?</h3><p>Un proyecto pensado para organizar vencimientos y ayudarte a reducir desperdicios.</p></article></div>
       <div class="space-top-25">{link('Ver novedades','novedades/','btn btn-plain','arrow-right')}</div></div></section>
    <section class="cta-section"><div class="container"><div class="cta-panel"><div><span class="eyebrow">Hablemos de soluciones</span><h2>¿Tienes una idea o necesitas ayuda?</h2><p>Encuentra respuestas, consulta el estado de nuestras apps y descubre cómo contactar con el equipo.</p></div>
      {link('Ir a soporte','soporte/','btn btn-primary','arrow-right')}</div></div></section>'''


def applications():
    return section_hero('Nuestras aplicaciones','Soluciones pequeñas.<br><span class="text-blue">Impacto cotidiano.</span>','Conoce las aplicaciones FREDDTECH y descubre en qué etapa se encuentra cada una.',[('Aplicaciones','aplicaciones/')]) + f'''<section class="section"><div class="container"><div class="app-grid">{app_card('box')}{app_card('calendar')}</div>
      <div class="status-info page-bottom"><strong>Nota de disponibilidad:</strong> «¿Dónde Quedó?» está en producción en Google Play. «¿Cuánto Queda?» continúa en planificación.</div>
    </div></section>'''


def app_detail(which):
    is_box = which == 'box'
    name = '¿Dónde Quedó?' if is_box else '¿Cuánto Queda?'
    quote = 'Menos buscar, más vivir.' if is_box else 'Menos desperdicio, más ahorro.'
    summary = 'Una aplicación Android para recordar dónde guardaste tus objetos y encontrarlos fácilmente.' if is_box else 'Una propuesta de aplicación Android para registrar productos, controlar fechas de caducidad y recibir recordatorios antes del vencimiento.'
    status = badge('En producción en Google Play' if is_box else 'En planificación / desarrollo','blue' if is_box else 'peach')
    feat = [
      ('Registro de objetos','Organiza la información sobre las cosas que deseas localizar.','box'),
      ('Ubicación de guardado','Recuerda el lugar donde dejaste cada objeto.','search'),
      ('Información visual','Utiliza referencias visuales cuando estén disponibles en la aplicación.','layers'),
      ('Búsqueda sencilla','Encuentra los registros que necesitas de forma práctica.','bolt')
    ] if is_box else [
      ('Control de productos','Planifica el registro de productos de uso cotidiano.','box'),
      ('Fechas de vencimiento','Consulta las fechas de caducidad registradas.','calendar'),
      ('Alertas oportunas','Funcionalidad prevista para avisar antes de vencer.','bell'),
      ('Menos desperdicio','Una ayuda para aprovechar mejor lo que ya tienes.','heart')
    ]
    grid = ''.join(f'<article class="feature"><span class="mini-icon">{ic(icon)}</span><h3>{title}</h3><p>{desc}</p></article>' for title,desc,icon in feat)
    extra = ('La aplicación se encuentra en producción en Google Play. Para consultas sobre disponibilidad, contacta con nuestro equipo de soporte.' if is_box else 'Las funciones descritas forman parte del concepto previsto y pueden cambiar durante el desarrollo. Todavía no existe una versión pública disponible.')
    return section_hero('Aplicación FREDDTECH',name,summary,[('Aplicaciones','aplicaciones/'),(name,'aplicaciones/'+('donde-quedo/' if is_box else 'cuanto-queda/'))]) + f'''<section class="section"><div class="container detail-grid">{app_visual(which,style='detail-art')}
      <div>{status}<h2 class="detail-headline">{quote}</h2><p>{summary}</p><p>{extra}</p>{play_button() if is_box else ""}
        <div class="fine-note"><strong>Recursos oficiales:</strong> {'Icono oficial de la aplicación. Las capturas se añadirán cuando estén disponibles.' if is_box else 'Espacio reservado para icono y capturas reales, que se añadirán cuando sean proporcionados.'}</div>
      </div></div></section>
      <section class="section section-warm"><div class="container"><div class="section-head"><span class="eyebrow">Cómo te ayuda</span><h2>{'Todo más fácil de encontrar.' if is_box else 'Lo importante, antes de vencer.'}</h2>
       <p>{'Conoce las funciones y capacidades de la aplicación.' if is_box else 'Estas son las principales funciones previstas para el producto.'}</p></div>
       <div class="feature-list">{grid}</div></div></section>
      <section class="section"><div class="container content-block"><h2>Disponibilidad y privacidad</h2><p>{extra}</p>
        <p>La documentación de privacidad específica de este producto tendrá su propio espacio oficial. No se publicarán políticas inventadas ni enlaces de descarga ficticios.</p>
        <p>¿Necesitas ayuda con {name}? Escribe a <a href="mailto:freddtech26@gmail.com">freddtech26@gmail.com</a>. El enlace abre tu aplicación de correo para que envíes el mensaje.</p>
        {link('Consultar información de privacidad','privacidad/'+('donde-quedo/' if is_box else 'cuanto-queda/'),'btn btn-secondary','arrow-right')}
      </div></section>'''


def about():
    return section_hero('Sobre FREDDTECH','Tecnología que <span class="text-blue">sirve para algo.</span>','FREDDTECH es una marca enfocada en desarrollar microaplicaciones y herramientas Android que solucionan necesidades específicas con sencillez y claridad.',[('Sobre FREDDTECH','nosotros/')]) + f'''<section class="section"><div class="container detail-grid"><div><span class="eyebrow">Nuestra filosofía</span><h2>Primero la necesidad. Después, la app.</h2><p>Creemos en soluciones digitales accesibles, de uso intuitivo y que aporten valor en pequeños momentos del día.</p><p>No se trata de sumar funciones sin sentido, sino de reducir pasos, ahorrar tiempo y ofrecer una experiencia agradable.</p></div>
    <div class="detail-art" aria-label="Representación abstracta de herramientas digitales"><div class="app-symbol">{ic('spark')}</div></div></div></section>
    <section class="section section-warm"><div class="container"><div class="section-head"><span class="eyebrow">Lo que nos guía</span><h2>Tres principios claros.</h2></div><div class="three-grid">
    <article class="mini-card"><span class="mini-icon">{ic('search')}</span><h3>Utilidad cotidiana</h3><p>Resolver problemas concretos con soluciones fáciles de entender.</p></article>
    <article class="mini-card"><span class="mini-icon">{ic('heart')}</span><h3>Personas primero</h3><p>Diseñar experiencias que se adapten a la vida real.</p></article>
    <article class="mini-card"><span class="mini-icon">{ic('shield')}</span><h3>Confianza</h3><p>Cuidar la calidad, la claridad y la privacidad desde el desarrollo.</p></article>
    </div></div></section>'''


def support():
    faqs = [
      ('¿Puedo descargar «¿Dónde Quedó?»?', 'Sí. Visita <a href="https://play.google.com/store/apps/details?id=com.freddtech.dondequedo">la ficha de ¿Dónde Quedó? en Google Play</a> para descargarla y consultar la disponibilidad en tu dispositivo o región.'),
      ('¿«¿Cuánto Queda?» está disponible?', 'No. El proyecto está en planificación/desarrollo; la web lo mostrará como «Próximamente» hasta que exista un lanzamiento real.'),
      ('¿Cómo solicito una nueva función?', 'Envía tu propuesta a <a href="mailto:freddtech26@gmail.com">freddtech26@gmail.com</a> e indica a qué aplicación corresponde.'),
      ('¿Cómo puedo reportar un error?', 'Escribe a <a href="mailto:freddtech26@gmail.com">freddtech26@gmail.com</a> e indica la aplicación, el problema, el modelo de dispositivo y los pasos para reproducirlo. No envíes contraseñas ni información sensible.'),
      ('¿Dónde encuentro la política de privacidad?', 'La sección Privacidad incluye un apartado independiente para cada aplicación. Enlazaremos allí los documentos oficiales una vez confirmados.'),
      ('¿Cómo obtengo ayuda con una compra Plus?', 'Para consultas sobre compras o restauración de beneficios, escribe a <a href="mailto:freddtech26@gmail.com">freddtech26@gmail.com</a>. Nunca compartas credenciales de Google Play.')
    ]
    items = ''.join(f'<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)
    return section_hero('Centro de soporte','Estamos aquí para <span class="text-blue">hacerlo simple.</span>','Consulta respuestas frecuentes y encuentra los canales de asistencia para nuestras aplicaciones.',[('Soporte','soporte/')]) + f'''<section class="section"><div class="container"><div class="section-head"><span class="eyebrow">Preguntas frecuentes</span><h2>Respuestas sin complicaciones.</h2></div>
      <div class="faq-grid">{items}</div></div></section>
      <section class="section section-warm"><div class="container"><div class="section-head"><span class="eyebrow">Contacta con FREDDTECH</span><h2>¿Necesitas ayuda específica?</h2><p>Escríbenos al correo oficial de soporte. El enlace abrirá tu aplicación de correo; revisa y envía el mensaje desde allí. Si no tienes una aplicación configurada, copia la dirección en tu servicio de correo.</p></div>
      <div class="contact-card"><div><h3>Correo de soporte</h3><p><a href="mailto:freddtech26@gmail.com">freddtech26@gmail.com</a></p></div><a class="btn btn-primary" href="mailto:freddtech26@gmail.com">Escribir un correo</a></div>
      <p class="small space-top-19">Para preparar un reporte, anota el nombre de la app, versión, dispositivo y una descripción del problema. Evita adjuntar datos sensibles.</p></div></section>'''


def privacy():
    return section_hero('Privacidad y documentación','Información clara.<br><span class="text-blue">Confianza real.</span>','Cada aplicación contará con su documentación de privacidad individual, publicada solo cuando sus textos y enlaces oficiales estén confirmados.',[('Privacidad','privacidad/')]) + f'''<section class="section"><div class="container"><div class="section-head"><span class="eyebrow">Documentos por aplicación</span><h2>Privacidad de la web y las aplicaciones.</h2><p>Consulta cómo tratamos la información al visitar este sitio.</p>{link('Privacidad y cookies de la web','privacidad/web/','btn btn-primary','arrow-right')}</div>
      <div class="policy-grid"><article class="policy-card">{badge('En producción','blue')}<h3 class="space-top-17">¿Dónde Quedó?</h3><p>Área reservada para la política oficial de privacidad de «¿Dónde Quedó?». Este sitio no sustituye el documento legal publicado para la app.</p>{link('Ver apartado de privacidad','privacidad/donde-quedo/','btn btn-secondary','arrow-right')}</article>
      <article class="policy-card">{badge('En planificación','peach')}<h3 class="space-top-17">¿Cuánto Queda?</h3><p>Espacio para la futura política de privacidad, que dependerá de las funciones y tratamientos de datos definitivos del producto.</p>{link('Ver apartado de privacidad','privacidad/cuanto-queda/','btn btn-secondary','arrow-right')}</article></div>
      <div class="status-info page-bottom"><strong>Importante:</strong> las secciones informativas pendientes no constituyen una política de privacidad legal. Antes de publicar un documento definitivo, verifica su contenido y enlace oficial.</div>
    </div></section>'''



def privacy_web():
    return section_hero('Privacidad de FREDDTECH WEB','Tu privacidad, <span class="text-blue">con claridad.</span>','Información sobre la navegación en este sitio, el contacto de soporte y la futura publicidad.',[('Privacidad','privacidad/'),('Privacidad de la web','privacidad/web/')]) + '''<section class="section"><div class="container content-block">
      <p class="small">Última actualización: 5 de noviembre de 2026.</p>
      <h2>Quién gestiona este sitio</h2><p>FREDDTECH publica información sobre sus aplicaciones en freddtech-web.pages.dev. Para consultas sobre privacidad o soporte, escribe a <a href="mailto:freddtech26@gmail.com">freddtech26@gmail.com</a>.</p>
      <h2>Información al navegar</h2><p>La web no tiene registro de usuarios, compras ni formularios de contacto. No incorpora Google Analytics. La página de Inicio incluye el código de Google AdSense y un bloque publicitario adaptable; su disponibilidad depende de la aprobación y del servicio de Google. La etiqueta de verificación de AdSense y el archivo ads.txt identifican nuestra cuenta de editor; por sí solos no muestran anuncios ni instalan cookies.</p>
      <p>Cloudflare Pages aloja y entrega el sitio. Al solicitar una página, su infraestructura procesa datos técnicos como la dirección IP, la URL solicitada y datos del navegador para entregar el contenido y proteger el servicio. Consulta la <a href="https://www.cloudflare.com/privacypolicy/">política de privacidad de Cloudflare</a> para conocer su tratamiento de datos.</p>
      <h2>Cuando nos escribes</h2><p>Los enlaces de correo abren tu aplicación o servicio de correo. Si envías un mensaje, recibimos la dirección del remitente y la información que incluyas para responder a tu consulta. El servicio de correo utilizado es Gmail, de Google. No envíes contraseñas, información de pago ni otros datos sensibles.</p>
      <p>Conservamos los mensajes mientras sean necesarios para atender la consulta y sus seguimientos o cumplir obligaciones aplicables. Puedes solicitar su eliminación escribiendo al mismo correo; atenderemos la solicitud en la medida que corresponda.</p>
      <h2>Publicidad y cookies</h2><p>Este sitio utiliza Google AdSense en Inicio. Hemos publicado un mensaje de consentimiento de Google para los visitantes a quienes corresponda. La integración está instalada; Google determina la disponibilidad de anuncios según la aprobación del sitio, las opciones de privacidad y la disponibilidad publicitaria.</p>
      <p>Google y sus proveedores publicitarios pueden utilizar cookies o almacenamiento similar para servir y medir anuncios, prevenir fraude y, cuando exista el consentimiento correspondiente, personalizar la publicidad a partir de visitas a este y otros sitios. Estos servicios pueden procesar identificadores, dirección IP, información del navegador e interacciones con anuncios.</p>
      <p>Puedes conocer <a href="https://policies.google.com/technologies/partner-sites?hl=es">cómo usa Google los datos de sitios asociados</a>, consultar su <a href="https://policies.google.com/privacy?hl=es">política de privacidad</a> y gestionar la personalización en <a href="https://myadcenter.google.com/">Mi centro de anuncios</a>. También puedes gestionar las cookies desde tu navegador.</p>
      <h2>Tus opciones y solicitudes</h2><p>Los visitantes a quienes corresponda verán el mensaje de consentimiento de Google y podrán aceptar, rechazar o gestionar sus opciones. Para cambiar esa decisión, visita <a href="../../#opciones-privacidad">Opciones de privacidad en Inicio</a>: el botón de gestión aparece cuando Google informa que su panel de consentimiento está disponible. Google también puede mostrar su propio enlace de opciones de privacidad. Si bloqueas los servicios de Google, el panel puede no cargarse; puedes gestionar las cookies desde tu navegador o contactarnos.</p>
      <p>Para solicitar acceso, corrección o eliminación de información que nos hayas enviado, o plantear una consulta sobre su uso, contacta con freddtech26@gmail.com. Revisaremos tu solicitud y los derechos que correspondan según la normativa aplicable.</p>
      <h2>Enlaces y aplicaciones</h2><p>Los servicios externos tienen sus propias políticas. Esta información se refiere al sitio web; las aplicaciones Android tienen su documentación independiente, accesible desde la sección Privacidad. Las condiciones de una aplicación no se sustituyen por esta página.</p>
      <h2>Cambios</h2><p>Actualizaremos esta página cuando cambien los servicios o el tratamiento de información, indicando la fecha de modificación.</p>
      </div></section>'''


def privacy_app(which):
    is_box = which == 'box'
    name = '¿Dónde Quedó?' if is_box else '¿Cuánto Queda?'
    text = ('Esta sección está preparada para enlazar la política de privacidad oficial existente de la aplicación. Por seguridad, el enlace se incorporará cuando se verifique su dirección actual y su contenido.' if is_box else 'La política específica se redactará cuando estén definidas las funcionalidades y el tratamiento de datos reales de la aplicación.')
    return section_hero('Documentación de privacidad',f'Privacidad de <span class="text-blue">{name}</span>',text,[('Privacidad','privacidad/'),(name,'privacidad/'+('donde-quedo/' if is_box else 'cuanto-queda/'))]) + f'''<section class="section"><div class="container content-block"><div class="info-box"><h2>Documento oficial pendiente de incorporar</h2>
      <p>{text}</p><p>No se presenta una política inventada ni se afirma que este texto cumpla requisitos legales o de Google Play.</p>
      <p>Al confirmar el documento oficial, puede añadirse aquí un enlace externo y una fecha de actualización comprobada.</p></div>
      <div class="page-bottom">{link('Volver a privacidad','privacidad/','btn btn-secondary','arrow-right')}</div></div></section>'''


def news():
    return section_hero('Novedades','Ideas que avanzan.<br><span class="text-blue">Apps que evolucionan.</span>','Un espacio para comunicar futuros lanzamientos, mejoras y noticias reales de nuestras aplicaciones.',[('Novedades','novedades/')]) + f'''<section class="section"><div class="container"><div class="news-list">
       <article class="news-card"><span class="kicker">Sitio web · En preparación</span><h3>Un nuevo hogar para FREDDTECH</h3><p>Esta primera versión reúne nuestras aplicaciones, filosofía, soporte y secciones de documentación en una sola experiencia.</p></article>
       <article class="news-card"><span class="kicker">Aplicación · En planificación</span><h3>¿Cuánto Queda?</h3><p>Un concepto para registrar productos, seguir fechas de caducidad y recibir avisos útiles antes de su vencimiento.</p></article>
       <article class="news-card"><span class="kicker">Aplicación · En producción</span><h3>¿Dónde Quedó?</h3><p>La app Android que ayuda a recordar dónde se guardaron los objetos ya está en producción en Google Play.</p></article>
       <article class="news-card"><span class="kicker">Próximas publicaciones</span><h3>Actualizaciones verificadas</h3><p>Publicaremos fechas y enlaces solo cuando existan anuncios oficiales confirmados. No se muestran cifras de usuarios ni estadísticas inventadas.</p></article>
      </div></div></section>'''


def terms():
    return section_hero('Información legal','Términos de uso <span class="text-blue">en preparación.</span>','Este apartado está reservado para la publicación de los términos de uso oficiales del sitio y, cuando corresponda, de los productos FREDDTECH.',[('Términos de uso','terminos/')]) + f'''<section class="section"><div class="container content-block"><div class="info-box"><h2>Aún no se ha publicado un documento legal definitivo</h2>
      <p>La versión inicial de esta web es informativa, sin cuentas, compras ni formularios de envío. Los términos definitivos requieren revisión antes de su publicación.</p>
      <p>Este aviso de preparación no sustituye unos términos de uso ni constituye asesoría legal.</p></div></div></section>'''


def render_page(slug, title, description, body, active=''):
    depth = len([p for p in slug.strip('/').split('/') if p])
    root = '../' * depth or './'
    normal_policy = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'none'; form-action 'none'"
    if slug == '':
        bootstrap = "document.addEventListener('DOMContentLoaded',()=>{for(const src of ['./assets/js/site.js','./assets/js/ads.js']){const s=document.createElement('script');s.src=src;document.head.appendChild(s);}});"
        digest = base64.b64encode(hashlib.sha256(bootstrap.encode()).digest()).decode()
        page_policy = f"script-src 'sha256-{digest}' 'strict-dynamic' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; form-action 'none'"
        page_scripts = f'<script>{bootstrap}</script>'
    else:
        page_policy = normal_policy
        page_scripts = f'<script src="{root}assets/js/site.js" defer></script>'
    nav_entries = [('Inicio','', 'home'),('Aplicaciones','aplicaciones/','apps'),('Nosotros','nosotros/','about'),('Novedades','novedades/','news'),('Soporte','soporte/','support')]
    nav = ''.join(f'<a class="nav-link {"nav-cta" if key=="support" else ""}" href="{root}{path}" {"aria-current=\"page\"" if active == key else ""}>{name}</a>' for name,path,key in nav_entries)
    html = f'''<!doctype html><html lang="es"><head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#F9F6F1"><meta name="color-scheme" content="light">
  <meta name="description" content="{escape(description,quote=True)}">
  <meta name="robots" content="index,follow">
  <meta name="google-adsense-account" content="ca-pub-1728686227442320">
  <meta property="og:type" content="website"><meta property="og:title" content="{escape(title,quote=True)}">
  <meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:locale" content="es_EC">
  <title>{escape(title)}</title>
  <link rel="icon" type="image/svg+xml" href="{root}assets/img/freddtech-symbol.svg?v=curva-1">
  <link rel="stylesheet" href="{root}assets/css/styles.css">
  <meta http-equiv="Content-Security-Policy" content="{page_policy}">
  {page_scripts}
</head><body><a class="skip-link" href="#contenido">Saltar al contenido</a>
  <header class="site-header"><div class="container nav-shell"><a class="brand" href="{root}" aria-label="FREDDTECH, volver al inicio">
    <img class="brand-symbol" src="{root}assets/img/freddtech-symbol.svg?v=curva-1" width="44" height="44" alt=""><span class="brand-label">FREDD<span class="brand-highlight">TECH</span><span class="brand-caption">Pequeñas apps. Grandes soluciones.</span></span></a>
    <button class="menu-toggle" type="button" aria-label="Abrir menú de navegación" aria-expanded="false" aria-controls="navegacion" data-menu-toggle>{ic('menu')}</button>
    <nav class="nav-links" id="navegacion" data-main-nav aria-label="Navegación principal">{nav}</nav>
  </div></header>
  <main id="contenido">{body}</main>
  {('<div class="container privacy-options" id="opciones-privacidad"><button class="btn btn-secondary" type="button" data-privacy-options hidden>Gestionar consentimiento</button><a href="./privacidad/web/">Información sobre privacidad y cookies</a></div>' if slug == '' else '')}
  <footer class="site-footer"><div class="container"><div class="footer-grid"><div class="footer-main">
    <a class="brand" href="{root}" aria-label="FREDDTECH, volver al inicio"><img class="brand-symbol" src="{root}assets/img/freddtech-symbol.svg?v=curva-1" width="44" height="44" alt=""><span class="brand-label">FREDD<span class="brand-highlight">TECH</span><span class="brand-caption">Pequeñas apps. Grandes soluciones.</span></span></a>
    <p class="footer-about">Pequeñas apps. Grandes soluciones. Tecnología práctica para resolver problemas reales de la vida cotidiana.</p></div>
    <div class="footer-col"><h3>Explora</h3><a href="{root}aplicaciones/">Aplicaciones</a><a href="{root}nosotros/">Sobre FREDDTECH</a><a href="{root}novedades/">Novedades</a></div>
    <div class="footer-col"><h3>Ayuda</h3><a href="mailto:freddtech26@gmail.com">freddtech26@gmail.com</a><a href="{root}soporte/">Centro de soporte</a><a href="{root}aplicaciones/donde-quedo/">¿Dónde Quedó?</a><a href="{root}aplicaciones/cuanto-queda/">¿Cuánto Queda?</a></div>
    <div class="footer-col"><h3>Legal</h3><a href="{root}#opciones-privacidad">Opciones de privacidad</a><a href="{root}privacidad/web/">Privacidad y cookies de la web</a><a href="{root}privacidad/">Privacidad</a><a href="{root}terminos/">Términos de uso</a></div>
  </div><div class="footer-bottom"><span>© <span data-year>2026</span> FREDDTECH. Pequeñas apps. Grandes soluciones.</span>
  <span>Hecho para simplificar lo cotidiano.</span></div></div></footer>
  </body></html>'''
    html = html.replace('{{ASSET}}', root).replace('{{ROOT}}', root)
    path = ROOT / slug / 'index.html' if slug else ROOT / 'index.html'
    path.parent.mkdir(parents=True,exist_ok=True)
    html = '\n'.join(line.rstrip() for line in html.splitlines()) + '\n'
    path.write_text(html, encoding='utf-8')
    return path


def main():
    pages=[
       ('','FREDDTECH — Pequeñas apps. Grandes soluciones.','FREDDTECH desarrolla aplicaciones Android sencillas que resuelven problemas cotidianos.', home(),'home'),
       ('aplicaciones','Aplicaciones Android | FREDDTECH','Explora las aplicaciones Android de FREDDTECH y sus estados de desarrollo.', applications(),'apps'),
       ('aplicaciones/donde-quedo','¿Dónde Quedó? | FREDDTECH','¿Dónde Quedó? te ayuda a recordar dónde guardaste tus objetos. App en producción en Google Play.', app_detail('box'),'apps'),
       ('aplicaciones/cuanto-queda','¿Cuánto Queda? | FREDDTECH','¿Cuánto Queda? es una app en planificación para fechas de caducidad y alertas.', app_detail('calendar'),'apps'),
       ('nosotros','Sobre FREDDTECH | Aplicaciones con propósito','Conoce la filosofía de FREDDTECH: aplicaciones Android útiles, simples y confiables.', about(),'about'),
       ('soporte','Soporte FREDDTECH | Ayuda y preguntas frecuentes','Encuentra respuestas sobre aplicaciones FREDDTECH, disponibilidad y soporte.', support(),'support'),
       ('privacidad','Privacidad y documentación | FREDDTECH','Secciones independientes para la documentación de privacidad de cada app FREDDTECH.', privacy(),''),
       ('privacidad/web','Privacidad y cookies de la web | FREDDTECH','Información sobre navegación, soporte, cookies y preparación de Google AdSense en FREDDTECH WEB.', privacy_web(),''),
       ('privacidad/donde-quedo','Privacidad de ¿Dónde Quedó? | FREDDTECH','Área informativa para enlazar la política oficial de privacidad de ¿Dónde Quedó?.', privacy_app('box'),''),
       ('privacidad/cuanto-queda','Privacidad de ¿Cuánto Queda? | FREDDTECH','Área informativa de privacidad para ¿Cuánto Queda?, en desarrollo.', privacy_app('calendar'),''),
       ('novedades','Novedades y próximos lanzamientos | FREDDTECH','Consulta los estados de desarrollo de las aplicaciones y novedades de FREDDTECH.', news(),'news'),
       ('terminos','Términos de uso | FREDDTECH','Sección en preparación para términos de uso oficiales FREDDTECH.', terms(),'')
    ]
    for data in pages:
       print(render_page(*data))
    # 404 sin redirigir automáticamente ni cargar recursos externos
    html = (ROOT/'index.html').read_text(encoding='utf-8')
    import re
    html = re.sub(r'<main id="contenido">.*?</main>', '<main id="contenido"><section class="section"><div class="container content-block"><span class="eyebrow">Error 404</span><h1>Página no encontrada.</h1><p>Es posible que el enlace haya cambiado o que la dirección no exista.</p><a class="btn btn-primary" href="./">Volver al inicio</a></div></section></main>', html, flags=re.S)
    html = re.sub(r'<meta http-equiv="Content-Security-Policy" content="[^"]*">', "<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'none'; form-action 'none'\">", html)
    html = re.sub(r'<script>.*?</script>', '<script src="./assets/js/site.js" defer></script>', html, flags=re.S)
    html = re.sub(r'<div class="container privacy-options".*?</div>', '', html, flags=re.S)
    html = html.replace('href="./', 'href="/').replace('src="./', 'src="/')
    html = html.replace('<title>FREDDTECH — Pequeñas apps. Grandes soluciones.</title>','<title>Página no encontrada | FREDDTECH</title>').replace('<meta name="robots" content="index,follow">','<meta name="robots" content="noindex,follow">')
    html = '\n'.join(line.rstrip() for line in html.splitlines()) + '\n'
    (ROOT/'404.html').write_text(html,encoding='utf-8')

if __name__=='__main__':
    main()
