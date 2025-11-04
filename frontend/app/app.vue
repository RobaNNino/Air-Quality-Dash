<template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtPage />
  </div>
</template>

<style>
/* Global, subtle iOS-like styling */
:root {
  --ios-bg: #f5f6f7;
  --ios-surface: #ffffff;
  --ios-text: #0a0a0a;
  --ios-muted: #6b7280;
  --ios-primary: #007aff; /* iOS blue */
  --ios-border: #e5e7eb;
  --radius: 16px;
}

html, body, #__nuxt, #__layout, .nuxt-root, .nuxt-app, .nuxt-container {
  height: 100%;
}

body {
  margin: 0;
  background: var(--ios-bg);
  color: var(--ios-text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

a { color: var(--ios-primary); text-decoration: none; }
a:hover { text-decoration: underline; }

.container {
  max-width: 920px;
  margin: 0 auto;
  padding: 20px;
}

.card {
  background: var(--ios-surface);
  border: 1px solid var(--ios-border);
  border-radius: var(--radius);
  box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.06);
}

.row { display: flex; gap: 16px; flex-wrap: wrap; }

.chip {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 4px 10px; border-radius: 999px; background: #f1f5f9; color: #111827; font-size: 12px;
}

.segmented {
  display: inline-flex; background: #e5e7eb; padding: 4px; border-radius: 12px; border: 1px solid var(--ios-border);
}
.segmented button {
  border: 0; background: transparent; padding: 8px 14px; border-radius: 8px; font-weight: 600; color: #374151; cursor: pointer;
}
.segmented button.active { background: #fff; color: #111827; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }

.muted { color: var(--ios-muted); }
</style>
