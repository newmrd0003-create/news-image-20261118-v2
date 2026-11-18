# THE WORLD — Wednesday, 18 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261118)

A one-image front page summing up 18 November 2026's world news in six
stories, drawn entirely with Python's PIL — no external images, no network.

## The six stories

1. **Quad meets in Manila** — Trump in Manila for Quad leaders' talks, the
   first stop of a three-day Asia trip ending in China; APEC leaders meet in
   Shenzhen on 18–19 November, and Xi, Trump and Putin meet there on
   Thursday 19 November.
2. **Britain sanctions settlement firms** — Foreign Secretary Ed Miliband
   announces asset freezes and director disqualifications on eight Israeli
   construction and property firms plus activist group Tzav 9, to protect
   the two-state solution.
3. **Canada–China extend trade deals** — Xi meets Carney in Shenzhen; China
   cuts tariffs on about C$400 million of Canadian pork and seafood, and
   Canada extends steel and aluminium remission measures by two years.
4. **Cyclone Akvan bears down** — a Severe Cyclonic Storm in the Bay of
   Bengal, forecast to cross the Andhra Pradesh and Yanam coasts around
   noon on 20 November, with winds 120–130 km/h gusting to 145 km/h.
5. **Dhoni calls time on IPL** — MS Dhoni ends his IPL playing career after
   five titles and 5,439 runs with Chennai Super Kings, and becomes the
   team's mentor from 2027.
6. **Amazon bets $7bn on green India** — $7 billion in renewable energy in
   India by 2030, on top of $4 billion already contracted; four new wind
   and solar projects totalling 934 MW, including a 234 MW wind farm in
   Karnataka, its largest wind project contracted in Asia.

## How to run

```sh
python3 gen_image.py   # renders entry.png (1024x1024 RGB, deterministic)
node main.ts           # copies entry.png to /output/entry.png
```

`main.ts` honours `MAKEFUN_OUTPUT_DIR` to change the output directory
(default `/output`). Both steps need no network and no extra packages
beyond Pillow for the generator and Node 22 for the copy step.

## Layout

Masthead **THE WORLD** with the 18 November 2026 dateline, a lead story
with a drawn skyline hero band, two stories in the second row and three
in the third, each with a small pictogram (scales, bar chart, cyclone
spiral, cricket bat and ball, wind turbine and sun). Footer:
"WEDNESDAY, 18 NOVEMBER 2026 — THE DAY IN SIX STORIES".
