from datetime import date

from flask import (
    Blueprint,
    render_template,
    current_app,
    flash,
    request,
    session,
    redirect,
    url_for
)

from flask_login import (
    current_user,
    login_required
)

from ..models import (
    db,
    Produtos,
    Carrinho,
    Usuario,
    Cupom,
    Pedido,
    Itens,
    status_acessorio ,
    UsosCupons
)

from ..services.frete import calcular_frete

from ..utils.datas import calcular_data_entrega

from ..rota_perfil.cupons import validar_cupom_checkout

bp_checkout = Blueprint(
    "checkout",
    __name__
)


def criar_pedido(
    usuario,
    subtotal,
    total_final,
    envio,
    data_entrega ,
    forma_pagamento , 
    cupom_usado=None
):
  
  print("=== CHECKOUT ===")
  print(request.form)
  print("===============")
  
  
  pedido = Pedido(
      usuaria=usuario.id_usuaria,
      total=total_final,
      status="Pendente",
      envio=envio,
      data_entrega=data_entrega , 
      forma_pagamento= forma_pagamento , 
      cupom_usado=cupom_usado
  )
  
  print("Usuária:", usuario.id_usuaria)
  print("Total:", total_final)
  print("Envio:", envio)
  print("Pagamento:", forma_pagamento)
  print("Cupom:", cupom_usado)

  print("ANTES DO COMMIT")
  db.session.add(pedido)
  db.session.flush()
  print("DEPOIS DO COMMIT")
  return pedido

def criar_itens_pedido(
    pedido,
    itens_carrinho
):
  for item in itens_carrinho:

      produto = Produtos.query.get(
          item.produto_id
      )

      if not produto:
          continue

      novo_item = Itens(
          pedido_id=pedido.id,
          produto_id=item.produto_id,
          quantidade=item.quantidade,
          preco_unit=produto.preco
      )

      db.session.add(novo_item)

      # ESTOQUE
      produto.em_estoque -= item.quantidade

      if produto.em_estoque <= 0:
        produto.em_estoque = 0
        produto.status = status_acessorio.VENDIDO

def limpar_carrinho(usuario_id):

    Carrinho.query.filter_by(
        usuario_id=usuario_id
    ).delete()


@bp_checkout.route("/checkout")
@login_required
def checkout():

    itens = Carrinho.query.filter_by(
        usuario_id=current_user.id_usuaria
    ).all()

    produtos_checkout = []
    subtotal = 0

    for item in itens:

        produto = Produtos.query.get(
            item.produto_id
        )

        if produto:

            produtos_checkout.append({
                "produto": produto,
                "quantidade": item.quantidade,
                "subtotal": produto.preco * item.quantidade
            })

            subtotal += (
                produto.preco *
                item.quantidade
            )

    cupom_id = session.get("cupom_id")

    cupom_valido = None
    desconto = 0
    valor_com_desconto = subtotal

    if cupom_id:
      cupom = Cupom.query.filter_by(
        id_cupom=cupom_id
      ).first()
      cupom_valido = validar_cupom_checkout(
        cupom)
    if cupom_valido:
      if cupom.tipo == "fixo":
        desconto = (
          cupom.valor_desconto
        )
      elif cupom.tipo == "porcentagem":
        desconto = (
          float(subtotal) *
          (
            cupom.valor_desconto/ 100
            )
        )
      valor_com_desconto = (
        float(subtotal) -desconto)
    
    end = current_user.enderecos[0]

    fretes = calcular_frete(end)

    return render_template(
        "checkout.html",
        produtos_checkout=produtos_checkout,
        enderecos=current_user.enderecos,
        subtotal=subtotal,
        desconto=desconto,
        valor_com_desconto=valor_com_desconto,
        cupom_aplicado=cupom_valido,
        cupons=current_user.cupons,
        fretes=fretes
    )

@bp_checkout.route(
    "/finalizar-compra",
    methods=["POST"]
)
@login_required
def finalizar_compra():
  print("Entrou no final da compra")
  print(request.form)
  itens_carrinho = Carrinho.query.filter_by(
    usuario_id=current_user.id_usuaria
    ).all()
    # Verifica estoque ANTES
  for item in itens_carrinho:
    produto = Produtos.query.get(
      item.produto_id
    )
    if not produto:
      continue
    if produto.em_estoque < item.quantidade:
        flash(
            f"{produto.nome} não possui estoque suficiente."
        )
        return redirect(
            url_for(
                "checkout.checkout"
            )
        )
  if not itens_carrinho:
      flash(
          "Carrinho vazio"
      )
      return redirect(
          url_for(
              "checkout.checkout"
          )
      )
  
  subtotal = 0
  
  for item in itens_carrinho:
  
      produto = Produtos.query.get(
          item.produto_id
      )
  
      if produto:
  
          subtotal += (
              produto.preco *
              item.quantidade
          )
  
  # TEMPORÁRIO
  total_final = subtotal
  
  cupom_id = session.get("cupom_id")

  cupom_nome = None
  
  if cupom_id:
    cupom = Cupom.query.filter_by(
        id_cupom=cupom_id
    ).first()
    cupom = validar_cupom_checkout(
        cupom
    )
    if cupom:
      cupom_nome = cupom.nome_cupom
      if cupom.tipo == "fixo":
        total_final -= float(
          cupom.valor_desconto
        )
      elif cupom.tipo == "porcentagem":
        total_final -= (
          float(subtotal)* (cupom.valor_desconto/ 100)
        )
  
  if total_final < 0:
    total_final = 0
  
  data_entrega = calcular_data_entrega()

  envio = request.form.get("horario")

  forma_pagamento = request.form.get("forma_pagamento")

  endereco_id = request.form.get("enderecos")
  frete = request.form.get("frete")
  
  print("FORMA PAGAMENTO:", forma_pagamento)
  print("ENVIO:", envio)
  print("ENDERECO:", endereco_id)
  print("FRETE:", frete)
  
  pedido = criar_pedido(
    usuario=current_user,
    subtotal=subtotal,
    total_final=total_final,
    envio=envio,
    data_entrega=data_entrega ,
    forma_pagamento=forma_pagamento,
    cupom_usado=cupom_nome
  )

  criar_itens_pedido(
    pedido,
    itens_carrinho
  )
  limpar_carrinho(
    current_user.id_usuaria
  )

  cupom_id= session.get("cupom_id")
  
  if cupom_id:
    uso = UsosCupons(
      cliente = current_user.id_usuaria ,
      cupom_id = cupom_id ,
    )
    db.session.add(uso)
    session.pop("cupom_id" , None)
  
  
  db.session.commit()
  
  flash(
      "Compra finalizada. Redirecionando..."
  )
  
  return redirect(
      url_for(
          "usuario.perfil"
      )
  )