<script setup>
const config = useRuntimeConfig()
const { data: stationsResponse, pending, error } = await useFetch(`${config.public.apiBase}/stations`)
const stations = computed(() => stationsResponse.value?.stations ?? [])
</script>

<template>
    <div style="padding:20px;font-family:sans-serif">
        <h1>Lista Stazioni</h1>

        <div v-if="pending">Caricamento...</div>
        <div v-if="error">Errore: {{ error.message }}</div>

        <ul v-if="stations">
            <li v-for="station in stations" :key="station.id">
                <NuxtLink :to="`/station/${station.id}`">{{ station.name ?? station.id }}</NuxtLink>
            </li>
        </ul>
    </div>
</template>
