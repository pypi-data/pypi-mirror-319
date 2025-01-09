#!/bin/bash

# Function to handle the jump command
scout_jump() {
    # Get the directory from scout
    local new_dir
    new_dir=$(scout jump "$@" --shell)
    
    # Check if we got a directory
    if [ $? -eq 0 ] && [ -n "$new_dir" ]; then
        # Actually change directory
        cd "$new_dir" || return 1
    fi
}

# Function to set up scout shell integration
scout_init() {
    # Add scout functions to shell
    alias scout_jump='scout_jump'
    
    # Create the main scout function
    scout() {
        local cmd="$1"
        shift
        
        case "$cmd" in
            "jump")
                scout_jump "$@"
                ;;
            *)
                command scout "$cmd" "$@"
                ;;
        esac
    }
    
    # Export the function
    export -f scout
    export -f scout_jump
}

# Initialize scout shell integration
scout_init 