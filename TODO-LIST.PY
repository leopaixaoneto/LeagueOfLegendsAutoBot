
# TODO rotina de Login via LCU

# * ROTINA de lobby->champSelect->Game->lobby FEITO

# * ROTINA de Itemsets FEITO

# TODO New account cycle

# TODO Redeem new account prizes

# TODO Level-Up Check


# TODO Tutorial Routine
#     TODO Tutorial 1
#     TODO Tutorial 2
#     TODO Tutorial 3


# */ TODO Disenchant Routine - FEITO
#! MATERIAL_key_fragment = lootId (/lol-loot/v1/player-loot)
#!
#! /lol-loot/v1/player-loot/{lootName}/redeem = redeem nas capsulas talvez?
#!
#! /lol-loot/v1/recipes/{recipeName}/craft
#!
#! recipeName = Recipe que quer fazer (encontra os nomes e recipes que da pra fazer nos endpoints:  GET /lol-loot/v1/recipes/initial-item/{lootId} e POST /lol-loot/v1/recipes/initial-item/{lootId})
#! playerLootList = Array [] com os ingredientes da recipe em string, ["item1", "item2"] ex:
#!
#!  recipeName = "CHEST_128_OPEN"
#!  playerLootList = ["CHEST_128"]
#!
#!  recipeName = "CHEST_320_OPEN"
#!  playerLootList = ["CHEST_320"]
#!
#!  recipeName = "MATERIAL_key_fragment_forge"
#!  playerLootList = ["MATERIAL_key_fragment"]
#!
#!  recipeName = "CHEST_generic_OPEN"
#!  playerLootList = ["CHEST_generic", "MATERIAL_key"]
#!
#!  recipeName = "CHAMPION_RENTAL_disenchant"
#!  playerLootList = ["CHAMPION_RENTAL_133"] <- pode ser qualquer CHAMPION_RENTAL
#!  playerLootList = ["CHAMPION_RENTAL_89"]
#!
