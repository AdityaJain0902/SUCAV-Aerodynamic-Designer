import numpy as np
#IRA Data at 14km, 
Temp_14km=212.15
P_14km=1.54e4
dens_14km=0.256
dens_sea=1.155
dyn_visc=1.39e-5
kin_visc=5.506e-5
vel_14km=291.96
m = float(input("Enter aircraft mass (kg): "))
g = 9.81
M=float(input("Enter Cruise Mach Number: "))
b = float(input("Enter wing span: "))
AR = float(input("Enter aspect ratio: "))
Ct = float(input("Enter tip chord: "))#tip length, for pure delta, = 0
Cr=(2*b/AR)-Ct #valid for swept(trapezoidal) as well as delta wings
Airfoil = input("Enter airfoil type (Biconvex / Double Wedge): ")
tc= float(input('Enter t/c ratio: '))
Taper=Ct/Cr
MAC = (2/3) * Cr * (1 + Taper + Taper**2) / (1 + Taper)
rLE_confirm = input("leading edge radius known?(Yes/No): ")
if rLE_confirm=='Yes':
     rLE = float(input("Enter leading edge radius: "))
else:
     rLE = 0.0025*MAC #since for supersonic airfoils, rLE and chord length ratio is between 0 and 0.25%
Fuselage_shape=input("Enter Fuselage Afterbody shape (Pointed / Truncated): ")
if Fuselage_shape=="Truncated":
       dia_confirm = input("max fuselage dia known?(Yes/No): ")
       if dia_confirm=='Yes':
               d_fuse = float(input("Enter fuselage diameter: "))
               d_base=float(input("Enter D_base at end of fuselage: "))
               #length of nose, center body and aftbody
               ln=float(input("Enter length of nose: "))
               la=float(input("Enter length of aftbody: "))
               L_fuse = la+ln
               fineness=L_fuse/d_fuse
       else:
               d_base=float(input("Enter D_base at end of fuselage: "))
               #length of nose, center body and aftbody
               ln=float(input("Enter length of nose: "))
               la=float(input("Enter length of aftbody: "))
               L_fuse = la+ln
               fineness = 14# from nicolai
               d_fuse = L_fuse/fineness
else:
     dia_confirm = input("max fuselage dia known?(Yes/No): ")
     if dia_confirm=='Yes':
               d_fuse = float(input("Enter fuselage diameter: "))
               d_base=0
               #length of nose, center body and aftbody
               ln=float(input("Enter length of nose: "))
               lc=float(input("Enter length of centerbody: "))
               la=float(input("Enter length of aftbody: "))
               L_fuse = la+lc+ln
               fineness=L_fuse/d_fuse
     else:
               d_base=0
               #length of nose, center body and aftbody
               ln=float(input("Enter length of nose: "))
               lc=float(input("Enter length of centerbody: "))
               la=float(input("Enter length of aftbody: "))
               L_fuse = la+lc+ln
               fineness = 14# from nicolai
               d_fuse = L_fuse/fineness

Nose_shape=input("Enter nose type (Ogive/Conical): ")
semivertex_angle_nose=float(input("Enter semivertex angle for nose(multiple of 5): "))
fN=ln/d_fuse
fA=la/d_fuse
Swet_Sref_ratio=float(input("Enter Swet/Sref: "))#f4=4,f106A=3.2,Avro VB1=2.8,F-16=4.67
if Ct==0: 
    Delta=np.arctan(4/AR)#assuming delta with zero taper
    Sref = (b * Cr) / 2  
    print('Delta=',Delta*57.3)
else:
     Delta_deg=float(input("Enter sweep angle of LE (in degrees): "))
     Delta = np.deg2rad(Delta_deg) 
     Sref = (b * (Cr+Ct)) / 2
     print('sweep angle of LE= ',Delta_deg)
Se_Sref_ratio=0.85 #exposed area
Mn=M*np.cos(Delta)
#print('Mn=',Mn)
beta=(M**2-1)**0.5
CdLE = (2.56 * rLE * AR * np.cos(Delta)**2) / (
        b * (1 + 1/(M**3 * np.cos(Delta)**3))
    )# or refer to pg 357 of pdf for more accurate 
if Airfoil=="Biconvex":
     B=16/3
else:
     B=4#symmetric double wedge
if Mn>=1:#supersonic LE
     print('supersonic LE')#multiply with se/sref, se refers to elevator area-DOUBT
     if rLE==0:
        Cdw=(B/beta)*((tc)**2)*Se_Sref_ratio
     else:
        Cdw=CdLE+(16/(3*beta))*((tc)**2)*Se_Sref_ratio
else:#subsonic LE
     print('subsonic LE')
     if rLE==0:
          Cdw=(B/np.tan(Delta))*(tc**2)*Se_Sref_ratio
     else:
          Cdw=CdLE+(((16/3)*((tc)**2))/np.tan(Delta))*Se_Sref_ratio
Cdw=Cdw+0.013
print('Cdw=',Cdw)

MAC = (2/3) * Cr * (1 + Taper + Taper**2) / (1 + Taper)
print('MAC=',MAC)
#supersonic drag due to lift(13.1.4)
if d_fuse/b <=0.35:
     F_wing_body_lift_interference_factor=6.57*d_fuse/b #pg 330 approximation nicolai
else:
     F_wing_body_lift_interference_factor=(14.6*d_fuse/b)-2.81
if AR>=0.5 and AR<=1:
        Clalpha_WB=(0.015+(0.016*(AR-0.5)))
        ClalphaM1=(0.016+(0.028*(AR-0.5)))
if AR>1 and AR<=2:
        Clalpha_WB=(0.023+(0.012*(AR-1)))
        ClalphaM1=(0.030+(0.029*(AR-1)))
if AR>2 and AR<=3:
        Clalpha_WB=(0.035+(0.003*(AR-2)))
        ClalphaM1=(0.059+(0.021*(AR-2)))
if AR>3 and AR<=4:
        Clalpha_WB=(0.038+(0.002*(AR-3)))
        ClalphaM1=(0.080+(0.01*(AR-3)))
# This is per degree
print('Claplha_wing_body=',Clalpha_WB)
Clalpha_wing=Clalpha_WB/(F_wing_body_lift_interference_factor)
print('Claplha_wing=',Clalpha_wing)
print('rle', rLE*100/MAC)
if 0<=Taper<0.25:
          if rLE*100/MAC<=0.3:
             K__upper=0.16-(0.3*rLE*100/MAC)
             K__lower=0.14-(0.33*rLE*100/MAC)
             K__=K__upper-(((K__upper-K__lower)/(0.25))*((Taper-0)))
          if 0.3<rLE*100/MAC<=0.4:
             K__upper=0.16-(0.3*rLE*100/MAC)
             K__lower=0.06-(0.067*rLE*100/MAC)
             K__=K__upper-(((K__upper-K__lower)/(0.25))*((Taper-0))) 
          if 0.4<rLE*100/MAC<=0.6:
             K__upper=0.06-(0.05*rLE*100/MAC)
             K__lower=0.06-(0.067*rLE*100/MAC)
             K__=K__upper-(((K__upper-K__lower)/(0.25))*((Taper-0)))     
if 0.25<=Taper<0.50:
          if rLE*100/MAC<=0.3:
             K__upper=0.14-(0.33*rLE*100/MAC)
             K__lower=0.1-(0.23*rLE*100/MAC)
             K__=K__upper-(((K__upper-K__lower)/(0.25))*((Taper-0.25)))
          if 0.3<rLE*100/MAC<=0.6:
             K__upper=0.06-(0.067*rLE*100/MAC)
             K__lower=0.042-(0.04*rLE*100/MAC)
             K__=K__upper-(((K__upper-K__lower)/(0.25))*((Taper-0.25)))
if 0.50<=Taper<=1:
          if rLE*100/MAC<=0.3:
             K__upper=0.1-(0.23*rLE*100/MAC)
             K__lower=0.082-(0.22*rLE*100/MAC)
             K__=K__upper-(((K__upper-K__lower)/(0.50))*((Taper-0.50)))
          if 0.3<rLE*100/MAC<=0.6:
             K__upper=0.042-(0.04*rLE*100/MAC)
             K__lower=0.013
             K__=K__upper-(((K__upper-K__lower)/(0.50))*((Taper-0.50)))

e = 2 / (2 - AR + np.sqrt(4 + AR**2 + (AR*np.tan(Delta) - 2)**2))
K_=1/(np.pi*e*AR)
print('K_ Induced Drag due to lift=',K_)
print('K__Viscous Drag due to lift=',K__)

if Mn>1:
      K=(1/(Clalpha_WB*57.3))#convert to radian
else:
      deltaN_m1=(1/(ClalphaM1*57.3))-K_-K__
      if deltaN_m1<0:# more suction effect
             deltaN_m1=0
      ratio_N=1#best approximate value from graph,fig 13.7
      K=(1/(Clalpha_WB*57.3))-(ratio_N*deltaN_m1)
#print(ClalphaM1)
#print(1/ClalphaM1)
#print('deltaN_m1=',deltaN_m1)

#zero lift drag coefficient wing:
Cf_ratio=0.73
Re=dens_14km*MAC*M*vel_14km/dyn_visc
if Re<1e5:
    Cfi=1.328/((Re)**(1/2))
else:
    Cfi = 0.455 / ((np.log10(Re))**2.58)
Cf=Cf_ratio*Cfi
Cdf=Cf*Swet_Sref_ratio#supersonic skin fraction

Cd0_wing=Cdf+Cdw#zero lift drag of wing
print('Cd0_wing=',Cd0_wing)
print('K-Drag due to lift',K)# Drag due to lift
print("e=",e)
# FUSELAGE ZERO LIFT DRAG METHOD 1 RAYMER
#Re_fuse = dens_14km * vel_14km * L_fuse / dyn_visc
#if Re_fuse < 1e5:
    #Cf_fuse = 1.328 / (Re_fuse**0.5)
#else:
    #Cf_fuse = 0.455 / (np.log10(Re_fuse)**2.58)

# Fuselage wetted area (cylinder + correction)
#Swet_fuse = np.pi * d_fuse * L_fuse * (1 - (2/3)*(d_fuse/L_fuse))

#FF_fuse = 1 + 60/(fineness**3) + fineness/400 #from raymer section 12.5.2, form factor

# Fuselage drag coefficient
#Cd0_fuse = Cf_fuse * (Swet_fuse / Sref) * FF_fuse#add more terms 

#finding Cl
Lift=m*g

Cl =Lift/(0.5 * dens_14km * ((M*vel_14km)**2) * Sref)
print("Cl =", Cl)

#METHOD 2 FUSELAGE ZERO LIFT DRAG
#Detailed Cdo fuselage analysis, from FIG 13.16 nicolai
#Calculating Cdanc
if Fuselage_shape=="Pointed":
       if 0.1<=ln/la<=1:
              if 0<lc/la<0.2:
                     Cdanc_Upper=(2.4-(5.5*lc/la))/((2*la/d_fuse)**2)#upper refers to the equation at ln/la=0.5
              if 0.2<lc/la<0.4:
                     Cdanc_Upper=(1.8-(2.5*lc/la))/((2*la/d_fuse)**2) 
              if 0.4<lc/la:
                     Cdanc_Upper=(1.04-(0.6*lc/la))/((2*la/d_fuse)**2)

              if 0<lc/la<=0.4:
                     Cdanc_Lower=(1.3-(1.875*lc/la))/((2*la/d_fuse)**2)#lower refers to equation for ln/la=1
              if 0.4<lc/la:
                     Cdanc_Lower=(0.694-(0.36*lc/la))/((2*la/d_fuse)**2)                       
              Cdanc=Cdanc_Upper-(((Cdanc_Upper-Cdanc_Lower)/0.9)*((ln/la)-0.1))
       if 1<ln/la<=2:
              if 0<lc/la<=0.4:
                     Cdanc_Upper=(1.3-(1.875*lc/la))/((2*la/d_fuse)**2)#upper refers to equation for ln/la=1
              if 0.4<lc/la:
                     Cdanc_Upper=(0.694-(0.36*lc/la))/((2*la/d_fuse)**2)

              Cdanc_Lower=(0.6-(0.357*lc/la))/((2*la/d_fuse)**2)#lower refers to equation for ln/la=2
             
              Cdanc=Cdanc_Upper-(((Cdanc_Upper-Cdanc_Lower))*((ln/la)-1))

if Fuselage_shape=="Truncated":#FIG 13.17
       if 0.1<=ln/la<=1:
              Cdanc_Upper=(2.2-(2.2*((d_base/d_fuse)**2)))/((2*la/d_fuse)**2)#upper refers to equation for ln/la=0.5

              Cdanc_Lower=(1.2-(1.2*((d_base/d_fuse)**2)))/((2*la/d_fuse)**2)#lower refers to equation for ln/la=1
              
              Cdanc=Cdanc_Upper-(((Cdanc_Upper-Cdanc_Lower)/0.9)*((ln/la)-0.1))

       if 1<ln/la<=2:
              Cdanc_Upper=(1.2-(1.2*((d_base/d_fuse)**2)))/((2*la/d_fuse)**2)#upper refers to equation for ln/la=1

              Cdanc_Lower=(0.5-(0.5*((d_base/d_fuse)**2)))/((2*la/d_fuse)**2)#lower refers to equation for ln/la=2
              
              Cdanc=Cdanc_Upper-(((Cdanc_Upper-Cdanc_Lower))*((ln/la)-1))
print("Cdanc= ", Cdanc)
#Calculating CdN2, fig 13.20
if Nose_shape=="Ogive":
       if semivertex_angle_nose<=20:
              Kn=(20/1.02)*semivertex_angle_nose
       if 20<semivertex_angle_nose<=40:
              Kn=0.97+(semivertex_angle_nose/400)
       if 40<semivertex_angle_nose<=90:
              Kn=0.838+(0.0058*semivertex_angle_nose)
       if 0.5<=fN<=1:
          if beta/fN <1:
            CdN2_lower=(0.2+(0.1)*(beta/fN))/((fN**2+(1/4))*Kn)
            CdN2_upper=(0.2+(0.45)*(beta/fN))/((fN**2+(1/4))*Kn)
            CdN2=CdN2_upper-((CdN2_upper-CdN2_lower)*(fN-0.5)/(0.5))
          if fN/beta<=1:
            CdN2_lower=(0.63-(0.33)*(fN/beta))/((fN**2+(1/4))*Kn) 
            CdN2_upper=0.67/((fN**2+(1/4))*Kn)  
            CdN2=CdN2_upper-((CdN2_upper-CdN2_lower)*(fN-0.5)/(0.5))
       if 1<fN<=2.5:
          if beta/fN <=0.4:
            CdN2_lower=(0.2+(0.45)*(beta/fN))/((fN**2+(1/4))*Kn)
            CdN2_upper=(0.3+(1.75)*(beta/fN))/((fN**2+(1/4))*Kn)
            CdN2=CdN2_upper-((CdN2_upper-CdN2_lower)*(fN-1)/(1.5))
          if 0.4<beta/fN<=1:
            CdN2_lower=(0.2+(0.45)*(beta/fN))/((fN**2+(1/4))*Kn)
            CdN2_upper=(1.15-(0.3)*(beta/fN))/((fN**2+(1/4))*Kn)
            CdN2=CdN2_upper-((CdN2_upper-CdN2_lower)*(fN-1)/(1.5))
          if fN/beta<=1:
            CdN2_lower=0.67/((fN**2+(1/4))*Kn) 
            CdN2_upper=(0.63+(0.22)*(fN/beta))/((fN**2+(1/4))*Kn)
            CdN2=CdN2_upper-((CdN2_upper-CdN2_lower)*(fN-1)/(1.5))
       if fN>2.5:
         if beta/fN<=1:
            CdN2=(1.15-(0.3)*(beta/fN))/((fN**2+(1/4))*Kn)
         if fN/beta<1:
            CdN2=(0.63+(0.22)*(fN/beta))/((fN**2+(1/4))*Kn)
if Nose_shape=="Conical": # fig 13.19
       if semivertex_angle_nose==45:
            if beta/fN<=1:
             CdN2=(0.37+(0.06)*(beta/fN))/(fN**2+(1/4))
            else:
              CdN2=(0.6-(0.17)*(fN/beta))/(fN**2+(1/4))    
       if semivertex_angle_nose==40:
            if beta/fN<=1:
             CdN2=(0.4+(0.1)*(beta/fN))/(fN**2+(1/4))
            else:
             CdN2=(0.64-(0.14)*(fN/beta))/(fN**2+(1/4))
       if semivertex_angle_nose==35:
            if beta/fN<=1:
             CdN2=(0.45+(0.16)*(beta/fN))/(fN**2+(1/4))
            else:
             CdN2=(0.7-(0.09)*(fN/beta))/(fN**2+(1/4))    
       if semivertex_angle_nose==30:
            if beta/fN<=1:
             CdN2=(0.52+(0.23)*(beta/fN))/(fN**2+(1/4))
            else:
             CdN2=(0.55+(0.2)*(fN/beta))/(fN**2+(1/4))  
       if semivertex_angle_nose==25:
            if beta/fN<=0.8:
              CdN2=(0.62+(0.2875)*(beta/fN))/(fN**2+(1/4))
            if 0.8<beta/fN<=1:
              CdN2=(0.85-(0.2)*(beta/fN-0.8))/(fN**2+(1/4))
            if fN/beta<1:
              CdN2=(0.55+(0.2)*(fN/beta))/(fN**2+(1/4))  
       if semivertex_angle_nose==20:
            if beta/fN<=0.5:
              CdN2=(0.75+(0.54)*(beta/fN))/(fN**2+(1/4))
            if 0.5<beta/fN<=1:
              CdN2=(1.02-(0.52)*(beta/fN-0.5))/(fN**2+(1/4))
            if fN/beta<1:
              CdN2=(0.55+(0.2)*(fN/beta))/(fN**2+(1/4))  
       if semivertex_angle_nose==15:
            if beta/fN<=0.3:
              CdN2=(0.97+(0.9)*(beta/fN))/(fN**2+(1/4))
            if 0.3<beta/fN<=1:
              CdN2=(1.24-(0.714)*(beta/fN-0.3))/(fN**2+(1/4))     
            if fN/beta<1:
              CdN2=(0.55+(0.2)*(fN/beta))/(fN**2+(1/4))  
print("CdN2= ", CdN2)            
#Calculating CdA: Afterbody wave drag
#OGIVE and CONICAL- very similar values, except at some points, thus ogive boattails is taken for reference

if 0.6<d_base/d_fuse<=1:
          if beta/fA<=1:
               CdA_lower=(0.27-(0.22*beta/fA))/(fA**2)
               CdA_upper=(0.72-(0.52*beta/fA))/(fA**2)
               CdA=CdA_upper-((CdA_upper-CdA_lower)*((d_base/d_fuse)-0.6)/(0.2))
          else:
              CdA_lower=(0.5*fA/beta)/(fA**2)
              CdA_upper=(0.05+0.214*((fA/beta)-0.3))/(fA**2)
              CdA=CdA_upper-((CdA_upper-CdA_lower)*((d_base/d_fuse)-0.6)/(0.2))
if 0.4<d_base/d_fuse<=0.6:
          if beta/fA<=1:
               CdA_lower=(0.72-(0.52*beta/fA))/(fA**2)
               CdA_upper=(1.05-(0.70*beta/fA))/(fA**2)
               CdA=CdA_upper-((CdA_upper-CdA_lower)*((d_base/d_fuse)-0.4)/(0.2))
          else:
               CdA_lower=(0.05+0.214*((fA/beta)-0.3))/(fA**2)
               CdA_upper=(0.1+(0.41*((fA/beta)-0.4)))/(fA**2)
               CdA=CdA_upper-((CdA_upper-CdA_lower)*((d_base/d_fuse)-0.4)/(0.2))
if 0.2<d_base/d_fuse<=0.4:
          if beta/fA<=1:
               CdA_lower=(1.05-(0.70*beta/fA))/(fA**2)
               CdA_upper=(1.15-(0.70*beta/fA))/(fA**2)
               CdA=CdA_upper-((CdA_upper-CdA_lower)*((d_base/d_fuse)-0.2)/(0.2))
          else:
               CdA_lower=(0.1+(0.41*((fA/beta)-0.4)))/(fA**2)
               CdA_upper=(0.2+(0.5*((fA/beta)-0.5)))/(fA**2)
               CdA=CdA_upper-((CdA_upper-CdA_lower)*((d_base/d_fuse)-0.2)/(0.2))
if 0<=d_base/d_fuse<=0.2:
          if beta/fA<=1:
               CdA_lower=(1.15-(0.70*beta/fA))/(fA**2)
               CdA_upper=(1.17-(0.67*beta/fA))/(fA**2)
               CdA=CdA_upper-((CdA_upper-CdA_lower)*((d_base/d_fuse))/(0.2))
          else:
               CdA_lower=(0.2+(0.5*((fA/beta)-0.5)))/(fA**2)
               CdA_upper=(0.21+(0.58*((fA/beta)-0.5)))/(fA**2)
               CdA=CdA_upper-((CdA_upper-CdA_lower)*((d_base/d_fuse))/(0.2))
print("CdA= ", CdA)
#CdB:Base drag term: due to flow separation over a blunt base
CpB=-0.15 #base pressure coeffs
CdB=-CpB*((d_base/d_fuse)**2)
print("CdB= ", CdB)
#Final Cd0_body
FF_fuse = 1.0 + 60.0/(fineness**3) + fineness/400.0

# Cd_skin = Cf * (Swet / Sref) * FF_fuse
Cd0_body_skin = Cf * Swet_Sref_ratio * FF_fuse

# wave/nose/afterbody terms (scale by frontal area / planform area)
frontal_area = np.pi * (d_fuse**2) / 4.0
wave_scale = frontal_area / Sref
Cd0_body_wave = (CdN2 + CdA + Cdanc) * wave_scale # + CdB MISSING

Cd0_body = Cd0_body_skin + Cd0_body_wave

print("Cd0_body (skin) =", Cd0_body_skin)
print("Cd0_body (wave) =", Cd0_body_wave)
print("Cd0 fuselage/body =", Cd0_body)
Cd0_total = Cd0_wing + Cd0_body
print("Total Cd0 =", Cd0_total)
Cd = Cd0_total + K * Cl**2
print("Total Cd =", Cd)
L_D_ratio=Cl/Cd
print('L/D ratio=',L_D_ratio)


