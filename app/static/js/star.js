// Pega o elemento canvas e seu contexto 2D
const canvas = document.getElementById('starfield');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let mouse = {
    x: undefined,
    y: undefined,
    radius: 200 // Raio de influência do mouse para ativar a geração
};

// --- Parâmetros que você pode ajustar ---
const STAR_COUNT = 1000;
const STAR_RADIUS_MAX = 1.3;
const ROTATION_SPEED = 0.00003;
const MAX_NEIGHBORS = 2;       // Cada estrela se conecta a no máximo 2 vizinhas
const CONSTELLATION_DEPTH = 3; // Profundidade da cadeia de conexões (quantos "saltos")
// ------------------------------------

let starsArray = [];

class Star {
    constructor(x, y, radius) {
        this.x = x; this.y = y; this.radius = radius;
        this.color = `rgba(255, 255, 255, ${0.7 + Math.random() * 0.3})`;
        this.neighbors = []; // Array para armazenar as vizinhas pré-calculadas

        // Propriedades para rotação
        const center = { x: canvas.width / 2, y: canvas.height / 2 };
        this.distFromCenter = Math.sqrt(Math.pow(x - center.x, 2) + Math.pow(y - center.y, 2));
        this.angle = Math.atan2(y - center.y, x - center.x);
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
    }

    update() {
        this.angle += ROTATION_SPEED;
        const center = { x: canvas.width / 2, y: canvas.height / 2 };
        this.x = center.x + this.distFromCenter * Math.cos(this.angle);
        this.y = center.y + this.distFromCenter * Math.sin(this.angle);
        this.draw();
    }
}

function init() {
    starsArray = [];
    const center = { x: canvas.width / 2, y: canvas.height / 2 };
    const spawnRadius = Math.sqrt(Math.pow(canvas.width, 2) + Math.pow(canvas.height, 2)) / 2;

    // 1. Criar todas as estrelas
    for (let i = 0; i < STAR_COUNT; i++) {
        const angle = Math.random() * 2 * Math.PI;
        const radius = spawnRadius * Math.sqrt(Math.random());
        const x = center.x + radius * Math.cos(angle);
        const y = center.y + radius * Math.sin(angle);
        const starRadius = Math.random() * STAR_RADIUS_MAX + 0.2;
        starsArray.push(new Star(x, y, starRadius));
    }

    // 2. Para cada estrela, encontrar suas vizinhas mais próximas
    for (let i = 0; i < starsArray.length; i++) {
        let distances = [];
        for (let j = 0; j < starsArray.length; j++) {
            if (i !== j) {
                let dx = starsArray[j].x - starsArray[i].x;
                let dy = starsArray[j].y - starsArray[i].y;
                let distance = Math.sqrt(dx * dx + dy * dy);
                distances.push({ index: j, distance: distance });
            }
        }
        distances.sort((a, b) => a.distance - b.distance);
        starsArray[i].neighbors = distances.slice(0, MAX_NEIGHBORS).map(d => d.index);
    }
}

function drawGeneratedConstellation() {
    if (mouse.x === undefined) return;

    // Encontrar a estrela mais próxima do mouse
    let closestStarIndex = -1;
    let minDistance = mouse.radius;

    for (let i = 0; i < starsArray.length; i++) {
        const dx = mouse.x - starsArray[i].x;
        const dy = mouse.y - starsArray[i].y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < minDistance) {
            minDistance = distance;
            closestStarIndex = i;
        }
    }

    if (closestStarIndex === -1) return;

    // Gerar uma constelação a partir da estrela mais próxima
    const linesToDraw = new Set();
    const visited = new Set();
    const queue = [{ index: closestStarIndex, depth: 0 }];
    visited.add(closestStarIndex);

    while (queue.length > 0) {
        const { index: currentIndex, depth: currentDepth } = queue.shift();
        
        if (currentDepth >= CONSTELLATION_DEPTH) continue;

        const currentStar = starsArray[currentIndex];
        for (const neighborIndex of currentStar.neighbors) {
            if (!visited.has(neighborIndex)) {
                visited.add(neighborIndex);
                const neighborStar = starsArray[neighborIndex];
                // Adiciona a linha (garante ordem para evitar duplicatas)
                const lineKey = [currentIndex, neighborIndex].sort((a, b) => a - b).join('-');
                linesToDraw.add({ start: currentStar, end: neighborStar });
                queue.push({ index: neighborIndex, depth: currentDepth + 1 });
            }
        }
    }

    // Desenhar as linhas com opacidade baseada na proximidade do mouse
    const opacity = 1 - (minDistance / mouse.radius);

    linesToDraw.forEach(line => {
        ctx.beginPath();
        ctx.moveTo(line.start.x, line.start.y);
        ctx.lineTo(line.end.x, line.end.y);
        ctx.strokeStyle = `rgba(255, 255, 255, ${opacity * 0.4})`; // Opacidade controlada
        ctx.lineWidth = 0.8;
        ctx.stroke();
    });
}

function animate() {
    requestAnimationFrame(animate);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (const star of starsArray) {
        star.update();
    }
    drawGeneratedConstellation();
}

// --- Event Listeners ---
window.addEventListener('mousemove', (event) => { mouse.x = event.x; mouse.y = event.y; });
window.addEventListener('mouseout', () => { mouse.x = undefined; mouse.y = undefined; });
window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; init(); });

init();
animate();