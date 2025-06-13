import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import i18n from 'i18next';
import translationDE from './locales/de/translation.json';

const resources = {
    de: { translation: translationDE },
};

i18n
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
        resources,
        fallbackLng: 'de',
        interpolation: {
            escapeValue: false, // React already escapes
        },
    });

export default i18n;
