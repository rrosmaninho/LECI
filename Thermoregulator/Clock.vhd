library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity Clock is
   port (clk     : in  std_logic;
			enable  : in  std_logic;
			timeOut : out unsigned(std_logic_vector(15 downto 0)));
end entity Clock;

architecture Behavioral of Clock is
	signal day_count    : unsigned(std_logic_vector(2 downto 0));
   signal hour_count   : unsigned(std_logic_vector(5 downto 0));
   signal minute_count : unsigned(std_logic_vector(6 downto 0));
	signal s_timeOut    : unsigned(std_logic_vector(15 downto 0));
	 
begin
   process(clk, enable)
   begin
      if enable = '1' then
         if rising_edge(clk) then
				if minute_count(3 downto 0) = "1001" then
					if minute_count = "1011001" then
						minute_count <= (others => '0');
						if hour_count = "100011" then
							if day_count = "111" then
								day_count <= (others => '0');
							else
								day_count <= day_count + "001";
							end if;
							hour_count <= (others => '0');
						elsif hour_count = "011001" then
							hour_count(5 downto 4) <= hour_count(5 downto 4) + "01";
							hour_count(3 downto 0) <= (others => '0');
						elsif hour_count = "001001" then
							hour_count(5 downto 4) <= hour_count(5 downto 4) + "01";
							hour_count(3 downto 0) <= (others => '0');
						else
							hour_count <= hour_count + "000001";
						end if;
					else
						minute_count(3 downto 0) <= (others => '0');
						minute_count(6 downto 4) <= minute_count(6 downto 4) + "001";
					end if;
				else
					minute_count <= minute_count + "000001";
				end if;
			end if;
		end if;
   end process;

	s_timeOut <= day_count & hour_count & minute_count;
	timeOut <= s_timeOut;
end architecture Behavioral;
