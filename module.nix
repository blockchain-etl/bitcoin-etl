{ config, lib, pkgs, ... }:

with lib;

let
  cfg = config.services.bitcoinetl;
in
{
  options.services.bitcoinetl = {
    enable = mkEnableOption "Bitcoin ETL service";

    package = mkOption {
      type = types.package;
      default = pkgs.bitcoin-etl;
      description = "The bitcoin-etl package to use.";
    };
  };

  config = mkIf cfg.enable {

    users = {
      users.bitcoin-etl = {
        isSystemUser = true;
        group = "bitcoin-etl";
        home = "/home/bitcoin-etl";
        createHome = true;
        homeMode = "755";
      };
      groups.bitcoin-etl = { };
    };

    systemd.timers.bitcoinetl = {
      description = "Timer for Bitcoin ETL Service";
      wantedBy = [ "timers.target" ];
      after = [ "bitcoinetl.service" ];
      timerConfig = {
        OnCalendar = "hourly";
        Unit = "bitcoinetl.service";
      };
    };

    systemd.services.bitcoinetl = {
      description = "Bitcoin ETL Service";
      # service should only run when scheduled, not when system is booted so no
      # wantedBy = [ "multi-user.target" ];
      after = [ "network.target" ];
      script = ''
        ${cfg.package}/bin/bitcoinetl \
          ${if cfg.exportBlocks then "--export-blocks" else "--no-export-blocks"} \
      '';

      serviceConfig = {
        Restart = "on-failure";
        MemoryDenyWriteExecute = true;
        ReadWriteDirectories = "/home/bitcoin-etl/";
        DynamicUser = true;
        User = "bitcoin-etl";
        Group = "bitcoin-etl";
      };
    }; # systemd.services.bitcoinetl
  }; # config
}
