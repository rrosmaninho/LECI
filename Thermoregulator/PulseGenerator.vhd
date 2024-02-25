library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;

entity PulseGenerator is
	port (clkIn    : in  std_logic;
		   acel     : in  std_logic_vector(1 downto 0);
		   pulseOut : out std_logic);
end PulseGenerator;

architecture Behavioral of PulseGenerator is
	constant clock_frequency : integer := 10;
	signal counter : integer range 0 to clock_frequency - 1;
	signal pulse : std_logic := '0';
  
begin
	process (clkIn, acel)
		variable full_period : integer := clock_frequency;
		variable half_period : integer := clock_frequency / 2;
	begin
		if rising_edge(clkIn) then
			case acel is
				when "00" => 
					full_period := clock_frequency * 60;
					half_period := clock_frequency * 30;

				when "01" =>  
					full_period := clock_frequency;
					half_period := clock_frequency / 2;

				when "10" =>  
					full_period := clock_frequency / 20;
					half_period := clock_frequency / 40;

				when "11" =>  
					full_period := clock_frequency / 120;
					half_period := clock_frequency / 240;
			end case;

			if (counter = full_period - 1) then
				pulseOut <= '0';
				counter <= 0;
			elsif (counter = half_period - 1) then
				pulseOut <= '1';
			end if;
			counter <= counter + 1;
		end if;
	end process;
end Behavioral;
