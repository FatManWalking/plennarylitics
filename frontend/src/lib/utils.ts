let textcolor: string;

import { goto } from '$app/navigation';

export const preserveScroll = (url: string) => {
    goto(url, {
        noScroll: true
    });
};

export function change_color(isDark: Writable<boolean>) {
    if (isDark) {
        textcolor = 'text-neutral-900';
    } else {
        textcolor = 'text-neutral-100';
    }

    return textcolor;
}