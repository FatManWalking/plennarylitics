// List of currently available parties to search for
type party = {
    name: string;
    color: string;
    id: number;
    technicalName: string;
};

export const parties: party[] = [
    {
        name: 'CDU / CSU',
        color: '#000000',
        id: 1,
        technicalName: 'CDU',
    },
    {
        name: 'SPD',
        color: '#E4002B',
        id: 2,
        technicalName: 'SPD',
    },
    {
        name: 'Bündnis 90 / GRÜNE',
        color: '#009D3E',
        id: 3,
        technicalName: 'GRUENE',
    },
    {
        name: 'FDP',
        color: '#FFCD00',
        id: 4,
        technicalName: 'FDP',
    },
    {
        name: 'AfD',
        color: '#00A1DE',
        id: 5,
        technicalName: 'AFD',
    },
    {
        name: 'Linke',
        color: '#FF6D00',
        id: 6,
        technicalName: 'LINKE',
    },
    {
        name: 'Sonstige',
        color: '#808080',
        id: 7,
        technicalName: 'SONSTIGE',
    },
];
