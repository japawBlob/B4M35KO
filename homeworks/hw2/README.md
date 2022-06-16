# ILP - Image unshredding

Nejtěžší bylo načíst data ve formátu, aby se s tím dobře pracovalo. Všechny hinty v zadání je třeba implementovat, jinak
nebude implementace dostatečně rychlá a bude to timeoutovat (nebo mě to minimálně timeautovalo).

Implementace není žádná turbodobrá. Pro matici proměnných používám 2D pole - teď bych to už udělal pomocí dictionary a 
příkazu addConstrs(n,n, ...) a přistupoval k prvkům jako X[i, j] spíš než X[i][j]

Odevzdanej úkol je totál mess. Pokud se chceš inspirovat, tak doporučuju soubor main.py v tomto adresáři. Avšak po 
refactoru jsem netestoval jestli stále funguje (ale jako mělo by)