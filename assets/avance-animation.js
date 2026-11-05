(function () {
    const textoSelector = '.avance-animado[data-porcentaje]';
    const barraSelector = '.avance-barra-animada[data-porcentaje]';
    const selector = `${textoSelector}, ${barraSelector}`;
    const duracion = 1200;

    function animarTexto(elemento, objetivo) {
        let inicio;

        function paso(ahora) {
            if (inicio === undefined) inicio = ahora;
            const progreso = Math.min((ahora - inicio) / duracion, 1);
            const ease = 1 - Math.pow(1 - progreso, 3);
            elemento.textContent = (objetivo * ease).toFixed(1) + '%';
            if (progreso < 1) requestAnimationFrame(paso);
        }

        requestAnimationFrame(paso);
    }

    function animarBarra(elemento, objetivo) {
        const barra = elemento.querySelector('.progress-bar, [role="progressbar"]');
        if (!barra) return false;

        barra.style.width = '0%';

        let inicio;

        function paso(ahora) {
            if (inicio === undefined) inicio = ahora;
            const progreso = Math.min((ahora - inicio) / duracion, 1);
            const ease = 1 - Math.pow(1 - progreso, 3);
            const valor = objetivo * ease;
            barra.style.width = `${valor}%`;
            barra.setAttribute('aria-valuenow', valor.toFixed(1));
            if (progreso < 1) requestAnimationFrame(paso);
        }

        requestAnimationFrame(paso);
        return true;
    }

    function animar(elemento) {
        if (elemento.dataset.animado === 'true') return;

        const objetivo = Number(elemento.dataset.porcentaje);
        if (!Number.isFinite(objetivo)) return;

        if (elemento.matches(textoSelector)) {
            elemento.dataset.animado = 'true';
            animarTexto(elemento, objetivo);
        } else if (animarBarra(elemento, objetivo)) {
            elemento.dataset.animado = 'true';
        }
    }

    function revisar(nodo) {
        if (nodo.nodeType !== Node.ELEMENT_NODE) return;
        if (nodo.matches(selector)) animar(nodo);
        nodo.querySelectorAll(selector).forEach(animar);
        const barra = nodo.closest(barraSelector);
        if (barra) animar(barra);
    }

    function iniciar() {
        revisar(document.body);
        new MutationObserver(cambios => {
            cambios.forEach(cambio => {
                cambio.addedNodes.forEach(revisar);
            });
        }).observe(document.body, { childList: true, subtree: true });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', iniciar, { once: true });
    } else {
        iniciar();
    }
})();
