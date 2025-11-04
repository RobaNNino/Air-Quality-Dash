<script setup>
import { ref, computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
    Chart as ChartJS,
    LineElement, PointElement, LinearScale, CategoryScale, Legend, Tooltip, Filler,
} from 'chart.js'

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Legend, Tooltip, Filler)

const route = useRoute()
const config = useRuntimeConfig()
const { data: stationResponse, pending, error } = await useFetch(`${config.public.apiBase}/stations/${route.params.id}`)
const station = computed(() => stationResponse.value)
const metrics = computed(() => station.value?.metrics ?? [])

// Toggle view: 'table' | 'charts'
const view = ref('table')

// Chart helpers
function buildChartData(metric) {
    const days = metric?.daily ?? []
    const labels = days.map(d => d.date)
    return {
        labels,
        datasets: [
            {
                label: 'Media',
                data: days.map(d => d.average),
                borderColor: '#007aff',
                backgroundColor: 'rgba(0,122,255,0.15)',
                pointRadius: 2,
                tension: 0.35,
                fill: true,
            },
            {
                label: 'Min',
                data: days.map(d => d.min),
                borderColor: '#10b981',
                backgroundColor: 'rgba(16,185,129,0.10)',
                pointRadius: 0,
                tension: 0.35,
                fill: false,
            },
            {
                label: 'Max',
                data: days.map(d => d.max),
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239,68,68,0.10)',
                pointRadius: 0,
                tension: 0.35,
                fill: false,
            },
        ],
    }
}

const baseChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { position: 'top', labels: { usePointStyle: true } },
        tooltip: { mode: 'index', intersect: false },
    },
    interaction: { mode: 'nearest', intersect: false },
    scales: {
        x: { grid: { display: false } },
        y: { grid: { color: 'rgba(0,0,0,0.06)' }, ticks: { precision: 0 } },
    },
}
</script>

<template>
    <div class="container">
        <NuxtLink to="/">← Torna alla lista</NuxtLink>

        <div v-if="pending" class="muted spacer-8">Caricamento…</div>
        <div v-else-if="error" class="error-text spacer-8">Errore: {{ error.message }}</div>

        <div v-else-if="station" class="spacer-8">
            <header class="detail-header">
                <h1 class="ios-title">{{ station.name ?? station.id }}</h1>
                <div class="segmented">
                    <button :class="{ active: view==='table' }" @click="view='table'">Tabella</button>
                    <button :class="{ active: view==='charts' }" @click="view='charts'">Grafici</button>
                </div>
            </header>

            <p class="muted address-line" v-if="station.address || station.location?.address">{{ station.address || station.location?.address }}</p>

            <div v-for="(metric, idx) in metrics" :key="metric.name ?? metric.type ?? idx" class="card metric-card">
                <div class="metric-header">
                    <div>
                        <h2 class="metric-title">{{ metric.name ?? metric.type ?? `Metrica ${idx + 1}` }}</h2>
                        <p class="muted metric-subtitle">Media ponderata ultimi 7 giorni: <strong class="subtitle-strong">{{ metric.weighted_average_last7 ?? 'N/A' }}</strong></p>
                    </div>
                </div>

                <div v-if="view==='table'" class="table-wrap">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Data</th>
                                <th>Min</th>
                                <th>Avg</th>
                                <th>Max</th>
                                <th>Campioni</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="day in metric.daily" :key="day.date">
                                <td>{{ day.date }}</td>
                                <td>{{ day.min }}</td>
                                <td>{{ day.average }}</td>
                                <td>{{ day.max }}</td>
                                <td>{{ day.sample_size }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div v-else class="chart-wrap">
                    <Line :data="buildChartData(metric)" :options="baseChartOptions" />
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.spacer-8 { margin-top: 8px; }
.error-text { color: #b91c1c; }

.detail-header { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 8px; }
.ios-title { margin: 0; font-size: 28px; font-weight: 800; }
.address-line { margin-top: 0; }

.metric-card { margin: 16px 0; padding: 16px; }
.metric-header { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.metric-title { margin: 0 0 6px; font-size: 18px; }
.metric-subtitle { margin: 0; }
.subtitle-strong { color: #111; }

.table-wrap { overflow: auto; margin-top: 12px; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th { text-align: left; font-weight: 700; padding: 8px; border-bottom: 1px solid var(--ios-border); }
.data-table td { padding: 8px; border-bottom: 1px solid var(--ios-border); }
.data-table th:nth-child(n+2), .data-table td:nth-child(n+2) { text-align: right; }

.chart-wrap { height: 280px; margin-top: 12px; }
</style>
