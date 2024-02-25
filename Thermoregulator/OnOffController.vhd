library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;

entity OnOffController is
  port(
    TAMB: in unsigned(8 downto 0);
    TREF: in unsigned(8 downto 0);
    delta: in unsigned(8 downto 0);
    ctrlSignal: out std_logic
  );
end entity OnOffController;

architecture Behavioral of OnOffController is
  signal TON: unsigned(8 downto 0);
  signal TOFF: unsigned(8 downto 0);
begin
  TON <= TREF - delta/2;
  TOFF <= TREF + delta/2;
  
  process(TAMB)
  begin
    if TAMB >= TOFF then
      ctrlSignal <= '0';
    elsif TAMB <= TON then
      ctrlSignal <= '1';
    end if;
  end process;
end architecture Behavioral;
