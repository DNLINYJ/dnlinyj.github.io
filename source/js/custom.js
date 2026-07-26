/* 小彩蛋们喵～ */
(function () {
  'use strict';

  /* 控制台欢迎 */
  console.log(
    '%c ฅ^•ﻌ•^ฅ 欢迎光临菜鸡の小窝喵～ ',
    'color:#fff;background:linear-gradient(90deg,#ff9ec7,#b58cf0);padding:6px 14px;border-radius:8px;font-size:14px;font-weight:bold;'
  );
  console.log('%c🌸 Action Precedes Motivation. 🌸', 'color:#ff7ea8;font-size:12px;');
  console.log(
    '%c   /\\_/\\\n  ( o.o )  < 逆向使我快乐\n   > ^ <',
    'color:#b58cf0;font-family:monospace;font-size:12px;'
  );

  /* 离开/回来 标题卖萌 */
  var originTitle = document.title;
  var titleTimer = null;
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) {
      if (titleTimer) clearTimeout(titleTimer);
      document.title = '(´•ω•̥`) 呜呜，你要去哪里喵…';
    } else {
      document.title = '(≧∇≦)ﾉ 欢迎回来喵！';
      titleTimer = setTimeout(function () {
        document.title = originTitle;
      }, 2000);
    }
  });
})();
