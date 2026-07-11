#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstring>

// Standard C-interface structure for cross-language data streaming via FFI
struct Player {
    int id;
    int cost;
    double performance_value;
    char position[8];
    char team[64]; // Expanded to 64 bytes to perfectly fit long flag emoji string sequences
};

extern "C" {
    // Exported symbol for Python ctypes mapping
    int execute_knapsack_optimization(
        Player* players, 
        int total_players, 
        int budget_limit, 
        int req_def, 
        int req_mid, 
        int req_fwd, 
        int* output_indices
    ) {
        // Multi-dimensional dynamic programming allocation tables
        // Time Complexity: O(N * W), Space Complexity: O(N * W)
        std::vector<std::vector<double>> dp(total_players + 1, std::vector<double>(budget_limit + 1, 0.0));

        for (int i = 1; i <= total_players; ++i) {
            int current_cost = players[i - 1].cost;
            double current_val = players[i - 1].performance_value;

            for (int w = 0; w <= budget_limit; ++w) {
                if (current_cost <= w) {
                    dp[i][w] = std::max(dp[i - 1][w], dp[i - 1][w - current_cost] + current_val);
                } else {
                    dp[i][w] = dp[i - 1][w];
                }
            }
        }

        // Backtracking state machine checking positional constraints & federation caps
        int w = budget_limit;
        int chosen_count = 0;
        
        int count_gk = 0, count_def = 0, count_mid = 0, count_fwd = 0;
        
        // Federation tracking array map (Enforces Max 3 players from any single country)
        char team_registry[50][64]; // Expanded to match struct width limits
        int team_counts[50] = {0};
        int unique_teams = 0;

        for (int i = total_players; i > 0; --i) {
            if (dp[i][w] != dp[i - 1][w]) {
                Player p = players[i - 1];
                
                // Track nation distribution limit
                int team_idx = -1;
                for (int t = 0; t < unique_teams; ++t) {
                    if (std::strcmp(team_registry[t], p.team) == 0) {
                        team_idx = t;
                        break;
                    }
                }
                if (team_idx == -1) {
                    std::strcpy(team_registry[unique_teams], p.team);
                    team_idx = unique_teams;
                    unique_teams++;
                }

                if (team_counts[team_idx] >= 3) {
                    continue; // Skip asset if national boundary conditions are violated
                }

                // Positional cell filtering logic
                bool asset_validated = false;
                std::string pos(p.position);

                if (pos == "GK" && count_gk < 1) {
                    count_gk++; asset_validated = true;
                } else if (pos == "DEF" && count_def < req_def) {
                    count_def++; asset_validated = true;
                } else if (pos == "MID" && count_mid < req_mid) {
                    count_mid++; asset_validated = true;
                } else if (pos == "FWD" && count_fwd < req_fwd) {
                    count_fwd++; asset_validated = true;
                }

                if (asset_validated) {
                    team_counts[team_idx]++;
                    output_indices[chosen_count++] = p.id;
                    w -= p.cost;
                }
            }
        }
        return chosen_count;
    }
}
