library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;

entity Counter is
    port (
        clk      : in std_logic;
        reset    : in std_logic;
        radiator : in std_logic;
        temp     : out std_logic_vector(8 downto 0)
    );
end Counter;

architecture Behavioral of Counter is
    signal count : unsigned(8 downto 0);
begin
    process(clk, reset)
    begin
        if reset = '1' then
            count <= (others => '0');
        elsif rising_edge(clk) then
            if radiator = '1' then
                count <= count + 1;
            else
                count <= count - 1;
            end if;
        end if;
    end process;

    temp <= std_logic_vector(count);
end Behavioral;
