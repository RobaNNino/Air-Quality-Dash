<script setup>
const route = useRoute()
const config = useRuntimeConfig()
const { data: stationResponse, pending, error } = await useFetch(`${config.public.apiBase}/stations/${route.params.id}`)
const station = computed(() => stationResponse.value)
const metrics = computed(() => station.value?.metrics ?? [])
</script>

<template>
    <div style="padding:20px;font-family:sans-serif">
        <NuxtLink to="/">← Torna alla lista</NuxtLink>

        <div v-if="pending">Caricamento...</div>
        <div v-if="error">Errore: {{ error.message }}</div>

        <div v-if="station">
            <h1>{{ station.name ?? station.id }}</h1>

            <div v-for="(metric, idx) in metrics" :key="metric.name ?? metric.type ?? idx" style="margin:16px 0">
                <h2>{{ metric.name ?? metric.type ?? `Metrica ${idx + 1}` }}</h2>
                <p>Media ponderata ultimi 7 giorni: <strong>{{ metric.weighted_average_last7 ?? 'N/A' }}</strong></p>

                <table border="1" cellpadding="6" cellspacing="0">
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
        </div>
    </div>
</template>
