import { writable } from 'svelte/store';

// initialize with the light theme, dawn
const isDark = writable(true)

export { isDark };