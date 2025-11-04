<script setup>
const config = useRuntimeConfig()
const { data: stationsResponse, pending, error } = await useFetch(`${config.public.apiBase}/stations`)
const stations = computed(() => stationsResponse.value?.stations ?? [])

// Helpers to read optional fields safely
function stationAddress(s) {
    return (
        s?.address || s?.location?.address || s?.meta?.address ||
        [s?.street, s?.city].filter(Boolean).join(', ') || null
    )
}

function stationCity(s) {
    return s?.city || s?.location?.city || s?.meta?.city || null
}

function stationCoords(s) {
    const lat = s?.lat ?? s?.latitude ?? s?.coords?.lat ?? s?.location?.lat
    const lon = s?.lon ?? s?.lng ?? s?.longitude ?? s?.coords?.lon ?? s?.location?.lon
    if (lat != null && lon != null) return `${Number(lat).toFixed(4)}, ${Number(lon).toFixed(4)}`
    return null
}
</script>

<template>
    <div class="container">
        <header class="page-header">
            <h1 class="ios-title">Stazioni</h1>
            <p class="muted subtitle">Elenco stazioni di monitoraggio qualità dell'aria</p>
        </header>

        <div v-if="pending" class="muted">Caricamento…</div>
        <div v-else-if="error" class="error-text">Errore: {{ error.message }}</div>

        <div v-else>
            <div class="row">
                <div v-for="station in stations" :key="station.id" class="card station-card">
                    <div class="card-top">
                        <div>
                            <div class="station-name">{{ station.name ?? station.id }}</div>
                            <div class="muted station-address">
                                <span v-if="stationAddress(station)">{{ stationAddress(station) }}</span>
                                <span v-else-if="stationCity(station)">{{ stationCity(station) }}</span>
                                <span v-else class="muted">Indirizzo non disponibile</span>
                            </div>
                        </div>
                        <NuxtLink :to="`/station/${station.id}`" aria-label="Apri dettagli" class="chevron-btn">➔</NuxtLink>
                    </div>

                    <div class="chip-row">
                        <span class="chip" v-if="station.metrics?.length">
                            <span class="chip-dot"></span>
                            {{ station.metrics.length }} metriche
                        </span>
                        <span class="chip" v-if="stationCoords(station)">📍 {{ stationCoords(station) }}</span>
                        <span class="chip" v-if="station.elevation">⛰️ {{ station.elevation }} m</span>
                    </div>

                    <div class="card-actions">
                        <NuxtLink :to="`/station/${station.id}`">Apri dettagli</NuxtLink>
                    </div>
                </div>
            </div>
        </div>
    </div>
  
</template>

<style scoped>
.page-header { margin: 6px 0 18px; }
.ios-title { margin: 0; font-size: 28px; font-weight: 800; }
.subtitle { margin: 6px 0 0; }

.station-card { flex: 1 1 280px; padding: 16px; min-width: 280px; }
.card-top { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.station-name { font-weight: 700; font-size: 18px; line-height: 1.2; }
.station-address { font-size: 13px; margin-top: 4px; }

.chevron-btn {
    display: inline-flex; align-items: center; justify-content: center;
    width: 36px; height: 36px; border-radius: 999px; border: 1px solid var(--ios-border); background: #fff;
}

.chip-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }
.chip-dot { width: 8px; height: 8px; border-radius: 50%; background: #10b981; display: inline-block; }

.card-actions { margin-top: 12px; }
.error-text { color: #b91c1c; }
</style>
