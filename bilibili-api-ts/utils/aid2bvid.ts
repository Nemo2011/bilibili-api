var table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF",
  tr: Record<string, any> = {};

for (var i = 0; i < 58; i++) {
  tr[table[i]] = i;
}

var s = [11, 10, 3, 8, 4, 6],
  xor = 177451812,
  add = 8728348608;

export function bvid2aid({bvid}: {bvid: string}) {
  var r = 0;
  for (var i = 0; i < 6; i++) {
    r += tr[bvid[s[i]]] * 58 ** i;
  }
  return ((r - add) ^ xor);
}

export function aid2bvid({aid}: {aid: number}) {
  aid = (aid ^ xor) + add;
  var r = "BV1  4 1 7  ".split("");
  for (var i = 0; i < 6; i++) {
    r[s[i]] = table[Math.floor(aid / 58 ** i) % 58];
  }
  return r.join("");
}
