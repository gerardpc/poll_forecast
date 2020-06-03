%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Reparteix escons
% 
% INPUTS:
% n_partits := numero de partits
% v_vots := vector de vots
% 
% OUTPUTS:
% v_diputats := vector d'escons per partit en ordre inicial
%
% gerd 10.11.17
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [v_diputats, v_vots_original] = calc_escons(n_partits, v_vots)
% definicions previes
v_vots_original = v_vots;
llindar = 0.03; % llindar electoral
total_vots = sum(v_vots); % suma per circumscripcions
v_diputats = zeros(n_partits, 1);

%% filtra partits que no superen llindar
total_vots_taula = repmat(total_vots, n_partits, 1);
frac_vot = v_vots./total_vots_taula;
v_vots(frac_vot < llindar) = 0;

%% Barcelona, 85 diputats
n_dip = 85;
n_circ = 1;
[taula_hondt] = calcula_taula(n_partits, n_circ, n_dip, v_vots);

% assign seats
[v_diputats_circumscripcio] = assign_seats(n_partits, n_dip, taula_hondt);
v_diputats = v_diputats + v_diputats_circumscripcio;

%% Girona 17 diputats
n_dip = 17;
n_circ = 2;
[taula_hondt] = calcula_taula(n_partits, n_circ, n_dip, v_vots);

% assign seats
[v_diputats_circumscripcio] = assign_seats(n_partits, n_dip, taula_hondt);
v_diputats = v_diputats + v_diputats_circumscripcio;

%% Lleida 15 diputats
n_dip = 15;
n_circ = 3;
[taula_hondt] = calcula_taula(n_partits, n_circ, n_dip, v_vots);

% assign seats
[v_diputats_circumscripcio] = assign_seats(n_partits, n_dip, taula_hondt);
v_diputats = v_diputats + v_diputats_circumscripcio;

%% Tarragona 18 diputats
n_dip = 18;
n_circ = 4;
[taula_hondt] = calcula_taula(n_partits, n_circ, n_dip, v_vots);

% assign seats
[v_diputats_circumscripcio] = assign_seats(n_partits, n_dip, taula_hondt);
v_diputats = v_diputats + v_diputats_circumscripcio;

%% Dibuixa els resultats en un grafic circular
pie(v_diputats);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calcula taula d'assignació d'Hondt
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function[taula_hondt] = calcula_taula(n_partits, n_circ, n_dip, v_vots)

circ_vots = v_vots(:, n_circ);
vots_1 = repmat(circ_vots, 1, n_dip);
dhondt_factor = repmat(linspace(1, n_dip, n_dip), n_partits, 1);
taula_hondt = vots_1./dhondt_factor;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calcula diputats assignats 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function[v_diputats_circumscripcio] = assign_seats(n_partits, n_dip, taula_hondt)

v_diputats_circumscripcio = zeros(n_partits, 1);
v_vots = taula_hondt(:, 1);

for seat = 1:n_dip
    max_val = max(max(taula_hondt));
    indx = find(taula_hondt == max_val);
    [row, col] = ind2sub(size(taula_hondt), indx);
    if length(row) > 1
        var_row = find(v_vots == max(v_vots(row)));
        col = col(row == var_row);
        row = var_row;
    end
    row = min(row);
    taula_hondt(row, col) = 0;
    v_diputats_circumscripcio(row) = v_diputats_circumscripcio(row) + 1;
end
end