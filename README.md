# monpedia
 
An external program for viewing MGQ Paradox monsterpedia.
For tracking down elusive recruits and materials.

Requires the following files from the decompiled game file: Armors.txt, Enemies.txt, Items.txt, Weapons.txt, Scripts/201 - Library(Enemy).rb, Enemies.rvdata2.
Except for the rvdata2 file all can be acquired from ArzorX's translation repo and can be hot-swapped as the translation progresses.
The rvdata2 is only used for acquiring drop tables and doesn't need updating, except when trtr adds new enemies.

Needs python3.8+ to run, uses ast, re, and tkinter libraries, but I believe those are installed by default.

What it can do:
- Display enemy drops, stealable items, location, and applicable slayer skills
- Search for enemies using name or id
- Search for enemies with a specific drop
- Show enemies in given location

To do:
- Location list
- Prom's jungle juice recipe list
- Recruitability
