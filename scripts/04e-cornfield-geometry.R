# Run from the book root: Rscript scripts/04e-cornfield-geometry.R
ink <- '#111827'; muted <- '#6B7280'; green <- '#2F6F4E'
gold <- '#B7791F'; rule <- '#C9D8CE'; wash <- '#F3F7F4'

# Fixed r: move along a line of slope r until w_S = 1.
png('images/04e-cornfield-fixed-r.png', width=1800, height=1300,
    res=200, pointsize=14, type='quartz', bg='white')
par(mar=c(4.8,4.5,2.5,1),family='sans',fg=ink,col=ink,xpd=NA)
plot.new(); plot.window(xlim=c(0,0.83),ylim=c(0,0.59),asp=1,xaxs='i',yaxs='i')
arrows(0,0,0.8,0,length=0.08,col=muted,lwd=1.3)
arrows(0,0,0,0.57,length=0.08,col=muted,lwd=1.3)
mtext('Cancer risk among nonsmokers',1,line=2.2,col=ink,cex=0.9)
mtext('Cancer risk among smokers',2,line=2.5,col=ink,cex=0.9)
B <- .05; Delta <- .45; r <- 3; wN <- .12
P <- c(B+wN*Delta,B+r*wN*Delta)
Q <- c(B+Delta/r,B+Delta)
segments(0,0,P[1],P[2],col=muted,lwd=2.5)
segments(0,0,Q[1],Q[2],col=green,lwd=2.5)
# Dashed right-angle path displays both coordinate increments.
segments(P[1],P[2],Q[1],P[2],col=rule,lty=2,lwd=1.6)
segments(Q[1],P[2],Q[1],Q[2],col=rule,lty=2,lwd=1.6)
arrows(P[1],P[2],Q[1],Q[2],col=gold,lwd=2.5,length=.09)
points(P[1],P[2],pch=21,bg=muted,col='white',lwd=1.5,cex=1.2)
points(Q[1],Q[2],pch=21,bg=green,col='white',lwd=1.5,cex=1.2)
text(P[1]+.015,P[2]-.045,expression((B+w[N]*Delta~','~B+r*w[N]*Delta)),adj=0,cex=.95)
text(Q[1]+.015,Q[2]+.02,expression((B+Delta/r~','~B+Delta)),adj=0,col=green,cex=1)
text(.34,.38,'Keep r fixed',adj=0,font=2,col=green,cex=1.08)
text(.34,.325,expression('Move right by'~~frac((1-r*w[N])*Delta,r)),adj=0,cex=.96)
text(.34,.25,expression('Move up by'~~(1-r*w[N])*Delta),adj=0,cex=.96)
text(.34,.185,expression('Slope of the move'==r),adj=0,col='#765014',cex=.96)
text(.34,.125,expression('Original slope:'~~RR<=r),adj=0,col=muted,cex=.96)
text(.34,.065,'The new ray from the origin is steeper.',adj=0,cex=.90,col=green)
text(-.015,-.015,'0',col=muted,cex=.85)
dev.off()

# RR = 11: feasible pairs above the joint-bound frontier.
png('images/04e-null-region-11.png',width=1500,height=1400,
    res=200,pointsize=14,type='quartz',bg='white')
par(mar=c(5.1,5.1,1.6,1.2),family='sans',fg=ink,col=ink,
    col.axis=muted,las=1,mgp=c(3.2,.7,0),tcl=-.2,pty='s')
plot.new(); plot.window(xlim=c(0,70),ylim=c(0,70),asp=1,xaxs='i',yaxs='i')
x0 <- 11*(70-1)/(70-11)
r <- seq(x0,70,length.out=1000)
s <- 11*(r-1)/(r-11)
polygon(c(r,70,x0),c(s,70,70),col='#E3EEE6',border=NA)
abline(v=11,h=11,col=gold,lty=2,lwd=1.5)
lines(r,s,col=green,lwd=2.8)
axis(1,at=c(0,11,20,40,60,70),col=rule)
axis(2,at=c(0,11,20,40,60,70),col=rule)
box(col=rule)
mtext(expression(r == w[S]/w[N]),side=1,line=2.6,cex=1)
mtext(expression(s == (B+Delta)/B),side=2,line=3,las=0,cex=1)
text(44,53,'Can explain RR = 11',col=green,font=2,cex=1.04)
text(44,48,expression(rs/(r+s-1)>=11),col=green,cex=1)
text(39,5.6,'Cannot explain RR = 11',col=muted,cex=.95)
text(8.8,63,expression(r==11),col='#765014',adj=1,cex=.9)
text(61,8.5,expression(s==11),col='#765014',cex=.9)
text(44,22.8,expression(rs/(r+s-1)==11),col=green,cex=.96)
E <- 11+sqrt(11^2-11)
points(E,E,pch=21,bg=gold,col='white',lwd=1.7,cex=1.45)
dev.off()
