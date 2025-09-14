const canvas = document.getElementById('starfield');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let mouse = {
    x: undefined,
    y: undefined,
    radius: 200 
};

const STAR_COUNT = 1000;
const STAR_RADIUS_MAX = 1.3;
const ROTATION_SPEED = 0.00003;
const MAX_NEIGHBORS = 2;       
const CONSTELLATION_DEPTH = 3; 
const EASE_FACTOR = 0.08;      

let starsArray = [];
let activeStarIndices = new Set(); 

class Star {
    constructor(x, y, radius) {
        this.x = x; this.y = y;
        this.radius = radius;
        this.originalRadius = radius; 
        this.color = `rgba(255, 255, 255, ${0.7 + Math.random() * 0.3})`;
        this.neighbors = [];

        const center = { x: canvas.width / 2, y: canvas.height / 2 };
        this.distFromCenter = Math.sqrt(Math.pow(x - center.x, 2) + Math.pow(y - center.y, 2));
        this.angle = Math.atan2(y - center.y, x - center.x);

        this.isBreathing = false;
        this.targetRadius = this.originalRadius;
        this.currentRadius = this.originalRadius;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.currentRadius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
    }

    update() {
        this.angle += ROTATION_SPEED;
        const center = { x: canvas.width / 2, y: canvas.height / 2 };
        this.x = center.x + this.distFromCenter * Math.cos(this.angle);
        this.y = center.y + this.distFromCenter * Math.sin(this.angle);

        this.currentRadius += (this.targetRadius - this.currentRadius) * EASE_FACTOR;
        
        this.draw();
    }
}

function init() {
    starsArray = [];
    const center = { x: canvas.width / 2, y: canvas.height / 2 };
    const spawnRadius = Math.sqrt(Math.pow(canvas.width, 2) + Math.pow(canvas.height, 2)) / 2;

    for (let i = 0; i < STAR_COUNT; i++) {
        const angle = Math.random() * 2 * Math.PI;
        const radius = spawnRadius * Math.sqrt(Math.random());
        const x = center.x + radius * Math.cos(angle);
        const y = center.y + radius * Math.sin(angle);
        const starRadius = Math.random() * STAR_RADIUS_MAX + 0.2;
        starsArray.push(new Star(x, y, starRadius));
    }

    for (let i = 0; i < starsArray.length; i++) {
        let distances = [];
        for (let j = 0; j < starsArray.length; j++) {
            if (i !== j) {
                let dx = starsArray[j].x - starsArray[i].x;
                let dy = starsArray[j].y - starsArray[i].y;
                distances.push({ index: j, distance: Math.sqrt(dx * dx + dy * dy) });
            }
        }
        distances.sort((a, b) => a.distance - b.distance);
        starsArray[i].neighbors = distances.slice(0, MAX_NEIGHBORS).map(d => d.index);
    }
}

function drawGeneratedConstellation() {
    let newActiveStarIndices = new Set();
    
    if (mouse.x !== undefined) {
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

        if (closestStarIndex !== -1) {
            const linesToDraw = [];
            const queue = [{ index: closestStarIndex, depth: 0 }];
            newActiveStarIndices.add(closestStarIndex);

            while (queue.length > 0) {
                const { index: currentIndex, depth: currentDepth } = queue.shift();
                if (currentDepth >= CONSTELLATION_DEPTH) continue;

                const currentStar = starsArray[currentIndex];
                for (const neighborIndex of currentStar.neighbors) {
                    if (!newActiveStarIndices.has(neighborIndex)) {
                        newActiveStarIndices.add(neighborIndex);
                        linesToDraw.push({ start: currentStar, end: starsArray[neighborIndex] });
                        queue.push({ index: neighborIndex, depth: currentDepth + 1 });
                    }
                }
            }

            const opacity = 1 - (minDistance / mouse.radius);
            linesToDraw.forEach(line => {
                ctx.beginPath();
                ctx.moveTo(line.start.x, line.start.y);
                ctx.lineTo(line.end.x, line.end.y);
                ctx.strokeStyle = `rgba(255, 255, 255, ${opacity * 0.4})`;
                ctx.lineWidth = 0.8;
                ctx.stroke();
            });
        }
    }

    starsArray.forEach((star, index) => {
        if (newActiveStarIndices.has(index)) {
            star.targetRadius = star.originalRadius * 2.5; 
        } else {
            star.targetRadius = star.originalRadius; 
        }
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

window.addEventListener('mousemove', (event) => { mouse.x = event.x; mouse.y = event.y; });
window.addEventListener('mouseout', () => { mouse.x = undefined; mouse.y = undefined; });
window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; init(); });

init();
animate();