# cpm-calismam-
graph LR
    %% Düğüm Stilleri Tanımlaması
    classDef normal fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef critical fill:#ffcccc,stroke:#ff0000,stroke-width:3px;

    %% Düğümler (Kutucuk içindeki değerler [ Erken | Geç ] zamanlardır)
    N1("[ 0 | 0 ]\nDüğüm 1"):::critical
    N2("[ 3 | 7 ]\nDüğüm 2"):::normal
    N3("[ 4 | 4 ]\nDüğüm 3"):::critical
    N4("[ 9 | 9 ]\nDüğüm 4"):::critical
    N5("[ 12 | 12 ]\nDüğüm 5\n(BİTİŞ)"):::critical

    %% Faaliyetler (Oklar) ve Süreleri
    N1 -- "A (Süre: 3)" --> N2
    N1 == "B (Süre: 4)" ==> N3
    N2 -- "C (Süre: 2)" --> N4
    N3 == "D (Süre: 5)" ==> N4
    N4 == "E (Süre: 3)" ==> N5

    %% Kritik Yolun Vurgulanması (Kalın Kırmızı Oklar)
    linkStyle 1 stroke:#ff0000,stroke-width:3px,color:red;
    linkStyle 3 stroke:#ff0000,stroke-width:3px,color:red;
    linkStyle 4 stroke:#ff0000,stroke-width:3px,color:red;
