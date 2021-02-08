import time
import copy

ADANCIME_MAX=4

def elem_identice(lista):
    if(len(set(lista))==1) :
        castigator = lista[0]
        if castigator!=Joc.GOL:
            return castigator
    return False

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    JMIN=None
    JMAX=None
    GOL='#'

    def __init__(self, nr_linii, nr_coloane, matr=None): #Joc()
        self.nr_linii = nr_linii
        self.nr_coloane = nr_coloane
        if matr:
            self.matr = matr
        else:
            self.matr = [Joc.GOL] * self.nr_coloane * self.nr_linii

    @classmethod
    def jucator_opus(cls, jucator):
        if jucator==cls.JMIN:
            return cls.JMAX
        else:
            return cls.JMIN  	

    def final(self):
        if Joc.GOL not in self.matr:
            rez_x = self.matr.count('x')
            rez_o = self.matr.count('0')
            if rez_x == rez_o:
                return "remiza"
            elif rez_x > rez_o:
                return 'x'
            else:
                return '0'
        else:
            return False

    def mutari(self, jucator):
        l_mutari=[]
        for i in range(len(self.matr)):
            if self.matr[i]==Joc.GOL:
                copie_matr=copy.deepcopy(self.matr)
                copie_matr[i]=jucator
                self.umple_matricea_dupa_mutare(copie_matr)
                l_mutari.append(Joc(self.nr_linii, self.nr_coloane, copie_matr))
        return l_mutari

    def umple_matricea_dupa_mutare(self, matr):
        inca_umplem = True
        vecini_linii = [-1, -1, -1, 0, 0, 1, 1, 1]
        vecini_coloane = [-1, 0, 1, -1, 1, -1, 0, 1]
        while inca_umplem:
            inca_umplem = False
            for linie in range(self.nr_linii):
                for coloana in range(self.nr_coloane):
                    if matr[linie * self.nr_coloane + coloana] == self.GOL:
                        nr_x = 0
                        nr_0 = 0
                        for index in range(8):
                            vecin_linie = vecini_linii[index] + linie
                            vecin_coloana = vecini_coloane[index] + coloana
                            if vecin_linie >= 0 and vecin_coloana >= 0 and vecin_linie < self.nr_linii and vecin_coloana < self.nr_coloane:
                                if matr[vecin_linie * self.nr_coloane + vecin_coloana] == 'x':
                                    nr_x += 1
                                elif matr[vecin_linie * self.nr_coloane + vecin_coloana] == '0':
                                    nr_0 += 1
                        if nr_x > nr_0 and nr_x >= 4:
                            matr[linie * self.nr_coloane + coloana] = 'x'
                            inca_umplem = True
                        elif nr_0 > nr_x and nr_0 >= 4:
                            matr[linie * self.nr_coloane + coloana] = '0'
                            inca_umplem = True

    # numarul total de elemente adaugate
    def scor_jucator_1(self, jucator):
        return self.matr.count(jucator)

    # incercam sa prioritizam influienta unei piese
    # calculam numarul de vecini care ar putea sa fie influientati
    # de umplerea une casute. (vecinii care sunt casute libere)
    def scor_jucator_2(self, jucator):
        vecini_linii = [-1, -1, -1, 0, 0, 1, 1, 1,]
        vecini_coloane = [-1, 0, 1, -1, 1, -1, 0, 1]
        scor = 0
        for linie in range(self.nr_linii):
            for coloana in range(self.nr_coloane):
                if self.matr[linie * self.nr_coloane + coloana] != jucator:
                    continue
                for index in range(8):
                    vecin_linie = vecini_linii[index] + linie
                    vecin_coloana = vecini_coloane[index] + coloana
                    if vecin_linie >= 0 and vecin_coloana >= 0 and vecin_linie < self.nr_linii and vecin_coloana < self.nr_coloane:
                        if self.matr[vecin_linie * self.nr_coloane + vecin_coloana] == Joc.GOL:
                            scor+=1
                scor += 1
        return scor


    def estimeaza_scor(self, adancime, functie_scor):
        t_final=self.final()
        #if (adancime==0):
        if t_final==self.__class__.JMAX : #self.__class__ referinta catre clasa instantei
            return (200+adancime)
        elif t_final==self.__class__.JMIN:
            return (-200-adancime)
        elif t_final=='remiza':
            return 0
        else:
            if functie_scor == 1:
                return (self.scor_jucator_1(self.__class__.JMAX) - self.scor_jucator_1(self.__class__.JMIN))
            else:
                return (self.scor_jucator_2(self.__class__.JMAX) - self.scor_jucator_2(self.__class__.JMIN))
            


    def __str__(self):
        sir="  |"
        for i in range(self.nr_coloane):
            sir+=str(i)+" "
        sir+="\n"
        sir+="-"*(self.nr_coloane+1)*2+"\n"
        for i in range(self.nr_linii): #itereaza prin linii
                sir+= str(i)+" |"+" ".join([str(x) for x in self.matr[self.nr_coloane*i : self.nr_coloane*(i+1)]])+"\n"
        return sir
            

class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    O instanta din clasa stare este un nod din arborele minimax
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    #TO DO 2
    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc=tabla_joc
        self.j_curent=j_curent
        
        #adancimea in arborele de stari
        self.adancime=adancime	
        
        #estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare=estimare
        
        #lista de mutari posibile (tot de tip Stare) din starea curenta
        self.mutari_posibile=[]
        
        #cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        # e de tip Stare (cel mai bun succesor)
        self.stare_aleasa=None


    def mutari(self):		
        l_mutari=self.tabla_joc.mutari(self.j_curent) #lista de informatii din nodurile succesoare
        juc_opus=Joc.jucator_opus(self.j_curent)

        #mai jos calculam lista de noduri-fii (succesori)
        l_stari_mutari=[Stare(mutare, juc_opus, self.adancime-1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari
        
    
    def __str__(self):
        sir= str(self.tabla_joc) + "(Joc curent:"+self.j_curent+")\n"
        return sir

            
""" Algoritmul MinMax """

def min_max(stare, functie_scor):
    #daca sunt la o frunza in arborele minimax sau la o stare finala
    if stare.adancime==0 or stare.tabla_joc.final() :
        stare.estimare=stare.tabla_joc.estimeaza_scor(stare.adancime, functie_scor)
        return stare
        
    #calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile=stare.mutari()

    #aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare=[min_max(x, functie_scor) for x in stare.mutari_posibile ] #expandez(constr subarb) fiecare nod x din mutari posibile
    


    if stare.j_curent==Joc.JMAX :
        #daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa= max(mutariCuEstimare, key= lambda x: x.estimare)
    else:
        #daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa=min(mutariCuEstimare, key= lambda x: x.estimare)
        
    stare.estimare=stare.stare_aleasa.estimare
    return stare
    

def alpha_beta(alpha, beta, stare, functie_scor):
    if stare.adancime==0 or stare.tabla_joc.final() :
        stare.estimare=stare.tabla_joc.estimeaza_scor(stare.adancime, functie_scor)
        return stare

    if alpha>beta:
        return stare #este intr-un interval invalid deci nu o mai procesez
    
    stare.mutari_posibile=stare.mutari()
        

    if stare.j_curent==Joc.JMAX :
        estimare_curenta=float('-inf')
        
        for mutare in stare.mutari_posibile:
            #calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua=alpha_beta(alpha, beta, mutare, functie_scor) #aici construim subarborele pentru stare_noua
            
            if (estimare_curenta<stare_noua.estimare):
                stare.stare_aleasa=stare_noua
                estimare_curenta=stare_noua.estimare
            if(alpha<stare_noua.estimare):
                alpha=stare_noua.estimare
                if alpha>=beta:
                    break

    elif stare.j_curent==Joc.JMIN :
        estimare_curenta=float('inf')
        #completati cu rationament similar pe cazul stare.j_curent==Joc.JMAX
        for mutare in stare.mutari_posibile:
            #calculeaza estimarea
            stare_noua=alpha_beta(alpha, beta, mutare, functie_scor) #aici construim subarborele pentru stare_noua
            
            if (estimare_curenta>stare_noua.estimare):
                stare.stare_aleasa=stare_noua
                estimare_curenta=stare_noua.estimare
            if(beta>stare_noua.estimare):
                beta=stare_noua.estimare
                if alpha>=beta:
                    break
        
    stare.estimare=stare.stare_aleasa.estimare

    return stare
    



def afis_daca_final(stare_curenta):
    final=stare_curenta.tabla_joc.final() #metoda final() returneaza "remiza" sau castigatorul ("x" sau "0") sau False daca nu e stare finala
    if(final):
        if (final=='remiza'):
            print("Remiza!")
        else:
            print("A castigat "+final)
            
        return True
        
    return False
        
    

def main():
    #initializare algoritm
    raspuns_valid=False

    while not raspuns_valid:
        tip_algoritm=input("Algoritmul folosit? (raspundeti cu 1 sau 2 sau 3 sau 4)\n 1.Minimax 1\n 2.Alpha-beta 1\n 3.Minimax 2\n 4.Alpha-beta 2\n")
        if tip_algoritm in ['1','2', '3', '4']:
            raspuns_valid=True
        else:
            print("Nu ati ales o varianta corecta.")

    functie_scor = 1 if tip_algoritm in ['1', '2'] else 2
    # dificultate joc
    raspuns_valid=False
    while not raspuns_valid:
        dificultate_algorithm=input("Dificultate algoritm? (raspundeti cu 1, 2 sau 3)\n 1.Incepator\n 2.Mediu\n 3.Avansat\n ")
        if dificultate_algorithm in ['1', '2', '3']:
            raspuns_valid=True
            if dificultate_algorithm == '1':
                ADANCIME_MAX = 2 if tip_algoritm in ['2', '4'] else 1
            elif dificultate_algorithm == '2':
                ADANCIME_MAX = 4 if tip_algoritm in ['2', '4'] else 2
            else:
                ADANCIME_MAX = 6 if tip_algoritm is ['2', '4'] else 3
        else:
            print('Nu ati ales o varianta corecta.')

    #initializare jucatori
    raspuns_valid=False
    while not raspuns_valid:
        Joc.JMIN=input("Doriti sa jucati cu x sau cu 0? ").lower()
        if (Joc.JMIN in ['x', '0']):
            raspuns_valid=True
        else:
            print("Raspunsul trebuie sa fie x sau 0.")
    Joc.JMAX= '0' if Joc.JMIN == 'x' else 'x'
    # expresie= val_true if conditie else val_false  (conditie? val_true: val_false)
    raspuns_valid=False
    while not raspuns_valid:
        nr_linii=input('Numarul de linii al tablei? (trebuie sa fie un numar intre 5 si 10) ')
        print(nr_linii)
        if nr_linii.isdigit() and int(nr_linii) >= 5 and int(nr_linii) <= 10:
            nr_linii = int(nr_linii)
            raspuns_valid=True
        else:
            print('Ati ales un numar de linii invalid.')

    raspuns_valid=False
    while not raspuns_valid:
        nr_coloane=input('Numarul de coloane al tablei? (trebuie sa fie un numar intre 5 si 10) ')
        if nr_coloane.isdigit() and int(nr_coloane) >= 5 and int(nr_coloane) <= 10:
            nr_coloane = int(nr_coloane)
            if nr_linii%2==0 or nr_coloane%2==0:
                raspuns_valid=True
            else:
                print('Numarul de coloane trebuie sa fie un numar par.')
        else:
            print('Ati ales un numar de coloane invalid.') 
    #initializare tabla
    tabla_curenta=Joc(nr_linii, nr_coloane); #apelam constructorul
    print("Tabla initiala")
    print(str(tabla_curenta))
    
    #creare stare initiala
    stare_curenta=Stare(tabla_curenta,'x',ADANCIME_MAX)

    while True :
        exit = input("Scrieti exit pentru a iesi sau apasati enter pentru a continua\n")
        if exit == 'exit':
            break
        if (stare_curenta.j_curent==Joc.JMIN):
        #muta jucatorul
            #preiau timpul in milisecunde de dinainte de mutare
            t_inainte=int(round(time.time() * 1000))

            print("Acum muta utilizatorul cu simbolul", stare_curenta.j_curent)
            raspuns_valid=False
            while not raspuns_valid:
                try:
                    linie=int(input("linie="))
                    coloana=int(input("coloana="))
                
                    if (linie in range(stare_curenta.tabla_joc.nr_linii) and coloana in range(stare_curenta.tabla_joc.nr_coloane)):
                        if stare_curenta.tabla_joc.matr[linie * stare_curenta.tabla_joc.nr_coloane + coloana] == Joc.GOL:					
                            raspuns_valid=True
                        else:
                            print("Exista deja un simbol in pozitia ceruta.")
                    else:
                        print("Linie sau coloana invalida.")		
            
                except ValueError:
                    print("Linia si coloana trebuie sa fie numere intregi")
                    
            #dupa iesirea din while sigur am valide atat linia cat si coloana
            #deci pot plasa simbolul pe "tabla de joc"
            stare_curenta.tabla_joc.matr[linie * stare_curenta.tabla_joc.nr_coloane + coloana]=Joc.JMIN
            stare_curenta.tabla_joc.umple_matricea_dupa_mutare(stare_curenta.tabla_joc.matr)
            
            #afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))
            #preiau timpul in milisecunde de dupa mutare
            t_dupa=int(round(time.time() * 1000))
            print("Jucatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
            timp_jucator = str(t_dupa-t_inainte)

            #TO DO 8a
            #testez daca jocul a ajuns intr-o stare finala
            #si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta)):
                break
                
                
            #S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)
        
        #--------------------------------
        else: #jucatorul e JMAX (calculatorul)
            #Mutare calculator
            
            print("Acum muta calculatorul cu simbolul", stare_curenta.j_curent)
            #preiau timpul in milisecunde de dinainte de mutare
            t_inainte=int(round(time.time() * 1000))

            #stare actualizata e starea mea curenta in care am setat stare_aleasa (mutarea urmatoare)
            if tip_algoritm in ['1', '3']:
                stare_actualizata=min_max(stare_curenta, functie_scor)
            else:
                stare_actualizata=alpha_beta(-500, 500, stare_curenta, functie_scor)
            stare_curenta.tabla_joc=stare_actualizata.stare_aleasa.tabla_joc #aici se face de fapt mutarea !!!
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))
            
            #preiau timpul in milisecunde de dupa mutare
            t_dupa=int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
            print("Calculatorul estimeaza ca are " + str(stare_curenta.tabla_joc.estimeaza_scor(1, functie_scor)) + " puncte")
            timp_pc = str(t_dupa-t_inainte)
            #print("Timpul total de gandire este "+str(t_dupa-t_total)+" milisecudne.")
            #TO DO 8b
            if (afis_daca_final(stare_curenta)):
                break
                
            #S-a realizat o mutare.  jucatorul cu cel opus
            stare_curenta.j_curent=Joc.jucator_opus(stare_curenta.j_curent)
        #print("In total s-a gandit "+ str(timp_jucator+timp_pc)+" milisecunde") # not good
if __name__ == "__main__" :
    main()