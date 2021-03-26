# Build Command:
```
cd cloud-management-batch ; mkdir -p mta_archives ; mbt build -p=cf -t=mta_archives --mtar=bat.mtar
```

# Deploy Command:
```
cf deploy mta_archives/bat.mtar -f
```

# Subsequent Build+Deploy Commands:
```
mbt build -p=cf -t=mta_archives --mtar=bat.mtar ; cf deploy mta_archives/bat.mtar -f
```

# Undeploy Command:
```
cf undeploy bat -f --delete-services
```
