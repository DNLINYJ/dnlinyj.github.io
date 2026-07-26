/* 樱花飘落特效 - 全屏 canvas 花瓣（时间基准，速度与刷新率无关） */
(function () {
  'use strict';
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var isMobile = /Android|webOS|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768;
  var COUNT = isMobile ? 12 : 26;
  var COLORS = ['#ffd7e6', '#ffc4dc', '#ffb0d1', '#ffe3ee', '#ffcce0'];

  var canvas = document.createElement('canvas');
  canvas.id = 'sakura-canvas';
  canvas.style.cssText = 'position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;z-index:999;';
  document.body.appendChild(canvas);
  var ctx = canvas.getContext('2d');

  var W, H;
  function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  /* 速度单位统一为 px/秒 或 弧度/秒 */
  function Petal(initial) {
    this.reset(initial);
  }
  Petal.prototype.reset = function (initial) {
    this.x = Math.random() * W;
    this.y = initial ? Math.random() * H : -20 - Math.random() * 60;
    this.size = 7 + Math.random() * 8;
    this.speedY = 24 + Math.random() * 28;          // 24~52 px/s，悠悠地落
    this.speedX = 5 + Math.random() * 9;            // 轻微向右飘
    this.swing = Math.random() * Math.PI * 2;
    this.swingSpeed = 0.5 + Math.random() * 0.9;    // 摇摆频率 rad/s
    this.swingRange = 30 + Math.random() * 50;
    this.rot = Math.random() * Math.PI * 2;
    this.rotSpeed = (Math.random() - 0.5) * 1.6;    // 自转 rad/s
    this.color = COLORS[(Math.random() * COLORS.length) | 0];
    this.opacity = 0.55 + Math.random() * 0.4;
    this.baseX = this.x;
  };
  Petal.prototype.update = function (dt) {
    this.y += this.speedY * dt;
    this.swing += this.swingSpeed * dt;
    this.x = this.baseX + Math.sin(this.swing) * this.swingRange;
    this.baseX += this.speedX * dt;
    this.rot += this.rotSpeed * dt;
    if (this.y > H + 30 || this.baseX > W + 80) this.reset(false);
  };
  Petal.prototype.draw = function () {
    var s = this.size;
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.rotate(this.rot);
    ctx.scale(1, 0.75 + 0.25 * Math.sin(this.swing * 2));
    ctx.globalAlpha = this.opacity;
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.moveTo(0, -s);
    ctx.bezierCurveTo(s * 0.75, -s * 0.5, s * 0.75, s * 0.5, 0, s * 1.1);
    ctx.bezierCurveTo(-s * 0.75, s * 0.5, -s * 0.75, -s * 0.5, 0, -s);
    ctx.fill();
    ctx.restore();
  };

  var petals = [];
  for (var i = 0; i < COUNT; i++) petals.push(new Petal(true));

  var running = true;
  var last = performance.now();
  document.addEventListener('visibilitychange', function () {
    running = !document.hidden;
    if (running) {
      last = performance.now();
      requestAnimationFrame(loop);
    }
  });

  function loop(now) {
    if (!running) return;
    if (typeof now !== 'number') now = performance.now();
    var dt = Math.min((now - last) / 1000, 0.05); // 封顶防跳变
    last = now;
    ctx.clearRect(0, 0, W, H);
    for (var i = 0; i < petals.length; i++) {
      petals[i].update(dt);
      petals[i].draw();
    }
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
})();
